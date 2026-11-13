#!/usr/bin/env python3

from argparse import ArgumentParser
from collections import defaultdict, deque
from copy import deepcopy
from itertools import combinations
from math import comb
from pathlib import Path
from sys import stdout

from ordered_set import OrderedSet
from tqdm import tqdm
from pokerkit import (
    Automation,
    BettingStructure,
    BoardDealing,
    CheckingOrCalling,
    CompletionBettingOrRaisingTo,
    Folding,
)
import numpy as np
import pokerkit as pk

from utilities import save_efg, save_efg_interp

AUTOMATIONS = (
    Automation.ANTE_POSTING,
    Automation.BET_COLLECTION,
    Automation.BLIND_OR_STRADDLE_POSTING,
    Automation.RUNOUT_COUNT_SELECTION,
    Automation.HAND_KILLING,
    Automation.CHIPS_PUSHING,
    Automation.CHIPS_PULLING,
)


def parse_args():
    parser = ArgumentParser()

    parser.add_argument('name')
    parser.add_argument('interp_path', nargs='?', type=Path)
    parser.add_argument('--traversal', default='dfs', choices=['bfs', 'dfs'])

    return parser.parse_args()


def deals(deck, dealings):
    if dealings:
        dealing, *dealings = dealings

        for combo in combinations(deck, dealing):
            for deal in deals(deck - combo, dealings):
                yield ''.join(combo), *deal
    else:
        yield ()


def deal_count(deck, dealings):
    deck_size = len(deck)
    count = 1

    for dealing in dealings:
        count *= comb(deck_size, dealing)
        deck_size -= dealing

    return count


def infoset(h):
    tokens = ['{}']
    actions = []

    for op in h.operations:
        if isinstance(op, BoardDealing):
            tokens.append('{}')
        elif isinstance(op, Folding):
            actions.append('f')
        elif isinstance(op, CheckingOrCalling):
            actions.append('c')
        elif isinstance(op, CompletionBettingOrRaisingTo):
            actions.append('r')

    tokens.append(''.join(actions))

    return ':'.join(tokens)


def bets(game, p, traversal):
    p_js = {}, {}
    A_js = {}, {}
    U = defaultdict(int)
    V = defaultdict(int)
    hs = deque([(game(), [None, None])])

    match traversal:
        case 'bfs':
            pop = hs.popleft
        case 'dfs':
            pop = hs.pop
        case _:
            raise ValueError('unknown traversal')

    while hs:
        h, sigmas = pop()

        if not h.status:
            U[tuple(sigmas)] = p * np.array(h.payoffs)
        elif h.can_show_or_muck_hole_cards(False):
            V[tuple(sigmas)] = p * h.total_pot_amount / 2
        elif (i := h.actor_index) is None:
            if h.can_burn_card():
                h.burn_card('??')

            if h.can_deal_hole():
                h.deal_hole('??' * len(h.street.hole_dealing_statuses))
            elif h.can_deal_board():
                h.deal_board('??' * h.street.board_dealing_count)
            else:
                raise AssertionError

            hs.append((h, sigmas))
        else:
            j = infoset(h)
            A_j = []
            h_primes = []

            if h.can_fold():
                h_prime = deepcopy(h)

                A_j.append('f')
                h_prime.fold()
                h_primes.append(h_prime)

            if h.can_check_or_call():
                h_prime = deepcopy(h)

                A_j.append('c')
                h_prime.check_or_call()
                h_primes.append(h_prime)

            if h.can_complete_bet_or_raise_to():
                h_prime = deepcopy(h)

                A_j.append('r')
                h_prime.complete_bet_or_raise_to()
                h_primes.append(h_prime)

            assert A_j

            p_js[i].setdefault(j, sigmas[i])
            A_js[i].setdefault(j, A_j)

            for a, h_prime in zip(A_j, h_primes):
                sigma_primes = sigmas.copy()
                sigma_primes[i] = (j, a)

                hs.append((h_prime, sigma_primes))

    return p_js, A_js, U, V


def main():
    args = parse_args()
    game = getattr(pk, args.name)(AUTOMATIONS)

    if game.betting_structure != BettingStructure.FIXED_LIMIT:
        raise ValueError('not FL')

    deck = OrderedSet(map(repr, game.deck))
    dealings = []

    for street in game.streets:
        if street.hole_dealing_statuses:
            assert not any(street.hole_dealing_statuses)
            assert not dealings
            assert not street.card_burning_status

            dealings.append(len(street.hole_dealing_statuses))
            dealings.append(len(street.hole_dealing_statuses))

        if street.board_dealing_count:
            assert street.card_burning_status

            dealings.append(street.board_dealing_count)

    deals_ = list(
        tqdm(deals(deck, dealings), total=deal_count(deck, dealings)),
    )
    p = 1 / len(deals_)
    p_js, A_js, U, V = bets(game, p, args.traversal)
    Sigmas = {}, {}
    p_js2 = {}, {}
    A_js2 = {}, {}
    interps = None if args.interp_path is None else ({}, {})

    def fmt(i, j, deal):
        return j.format(deal[i], *deal[2:])

    def sigma(i, j_a, deal):
        if j_a is None:
            sigma = 0
        else:
            j, a = j_a
            j_a = fmt(i, j, deal), a
            sigma = Sigmas[i].setdefault(j_a, len(Sigmas[i]) + 1)

        return sigma

    for deal in tqdm(deals_):
        for i in range(2):
            for j, p_j in p_js[i].items():
                j = fmt(i, j, deal)
                p_js2[i][j] = sigma(i, p_j, deal)

            for j, A in A_js[i].items():
                j = fmt(i, j, deal)
                A_j = []

                for a in A:
                    A_j.append(
                        Sigmas[i].setdefault((j, a), len(Sigmas[i]) + 1),
                    )

                A_js2[i].setdefault(j, A_j)

                if args.interp_path is not None:
                    interps[i].setdefault(j, A)

    class U2:
        def __len__(self):
            return len(deals_) * (len(U) + len(V))

        def items(self):
            (hand_type,) = game.hand_types

            for deal in deals_:
                holes = deal[:2]
                board = deal[2:]

                for (j_a1, j_a2), us in U.items():
                    j_a1 = sigma(0, j_a1, deal)
                    j_a2 = sigma(1, j_a2, deal)

                    yield (j_a1, j_a2), us

                h1 = hand_type.from_game(holes[0], ''.join(board))
                h2 = hand_type.from_game(holes[1], ''.join(board))

                if h1 < h2:
                    sign = -1
                elif h1 > h2:
                    sign = 1
                else:
                    sign = 0

                for (j_a1, j_a2), v in V.items():
                    j_a1 = sigma(0, j_a1, deal)
                    j_a2 = sigma(1, j_a2, deal)

                    yield (j_a1, j_a2), (sign * v, -sign * v)

    save_efg(p_js2, A_js2, U2(), stdout)

    if args.interp_path is not None:
        args.interp_path.parent.mkdir(parents=True, exist_ok=True)

        with open(args.interp_path, 'w') as file:
            save_efg_interp(interps, file)


if __name__ == '__main__':
    main()
