#!/usr/bin/env python3

from argparse import ArgumentParser, BooleanOptionalAction
from collections import defaultdict, deque
from functools import partial
from pathlib import Path
from sys import stdout

from open_spiel.python.egt.utils import game_payoffs_array
from pyspiel import GameType, load_game, load_tensor_game
import numpy as np

from utilities import write_efg, write_efg_interp, write_nfg, write_nfg_interp


def parse_args():
    parser = ArgumentParser()

    parser.add_argument('name')
    parser.add_argument('interp_path', nargs='?', type=Path)
    parser.add_argument('--prune', action=BooleanOptionalAction)
    parser.add_argument('--stream', action=BooleanOptionalAction)
    parser.add_argument('--traversal', default='dfs', choices=['bfs', 'dfs'])

    return parser.parse_args()


def main_nfg(gamma, interp_path):
    U = game_payoffs_array(gamma)

    write_nfg(U, stdout)

    if interp_path is not None:
        interps = []

        for i, m in enumerate(U.shape[1:]):
            interps.append(list(map(partial(gamma.action_name, i), range(m))))

        interp_path.parent.mkdir(parents=True, exist_ok=True)

        with open(interp_path, 'w') as file:
            write_nfg_interp(interps, file)


def main_efg(gamma, interp_path, prune, traversal):
    n = gamma.num_players()
    Sigmas = [{} for _ in range(n)]
    p_js = [{} for _ in range(n)]
    A_js = [{} for _ in range(n)]
    U = defaultdict(int)
    interps = None if interp_path is None else [{} for _ in range(n)]
    hs = deque([(gamma.new_initial_state, 1, [0] * n)])

    match traversal:
        case 'bfs':
            pop = hs.popleft
        case 'dfs':
            pop = hs.pop
        case _:
            raise ValueError('unknown traversal')

    while hs:
        h, p, sigmas = pop()
        h = h()

        if h.is_terminal():
            U[tuple(sigmas)] += p * np.array(h.returns())
        elif (i := h.current_player()) < 0:
            for a, p_prime in h.chance_outcomes():
                if p_prime or not prune:
                    hs.append((partial(h.child, a), p_prime * p, sigmas))
        else:
            j = h.information_state_string()
            A = h.legal_actions()
            A_j = [Sigmas[i].setdefault((j, a), len(Sigmas[i]) + 1) for a in A]

            assert 0 != len(A) == len(A_j)

            p_js[i].setdefault(j, sigmas[i])
            A_js[i].setdefault(j, A_j)

            if interp_path is not None:
                interp = list(map(h.action_to_string, A))

                interps[i].setdefault(j, interp)

            for a, a_j in zip(A, A_j):
                sigma_primes = sigmas.copy()
                sigma_primes[i] = a_j

                hs.append((partial(h.child, a), p, sigma_primes))

    write_efg(p_js, A_js, U, stdout)

    if interp_path is not None:
        interp_path.parent.mkdir(parents=True, exist_ok=True)

        with open(interp_path, 'w') as file:
            write_efg_interp(interps, file)


def main_efg2(gamma, interp_path, prune, traversal):
    n = gamma.num_players()
    Sigmas = [{} for _ in range(n)]
    p_js = [{} for _ in range(n)]
    A_js = [{} for _ in range(n)]
    count = 0
    interps = None if interp_path is None else [{} for _ in range(n)]
    hs = deque([(gamma.new_initial_state, [0] * n)])

    match traversal:
        case 'bfs':
            pop = hs.popleft
        case 'dfs':
            pop = hs.pop
        case _:
            raise ValueError('unknown traversal')

    while hs:
        h, sigmas = pop()
        h = h()

        if h.is_terminal():
            count += 1
        elif (i := h.current_player()) < 0:
            for a, p_prime in h.chance_outcomes():
                if p_prime or not prune:
                    hs.append((partial(h.child, a), sigmas))
        else:
            j = h.information_state_string()
            A = h.legal_actions()
            A_j = [Sigmas[i].setdefault((j, a), len(Sigmas[i]) + 1) for a in A]

            assert 0 != len(A) == len(A_j)

            p_js[i].setdefault(j, sigmas[i])
            A_js[i].setdefault(j, A_j)

            if interp_path is not None:
                interp = list(map(h.action_to_string, A))

                interps[i].setdefault(j, interp)

            for a, a_j in zip(A, A_j):
                sigma_primes = sigmas.copy()
                sigma_primes[i] = a_j

                hs.append((partial(h.child, a), sigma_primes))

    class U:
        def __len__(self):
            return count

        def items(self):
            hs = deque([(gamma.new_initial_state, 1, [0] * n)])

            match traversal:
                case 'bfs':
                    pop = hs.popleft
                case 'dfs':
                    pop = hs.pop
                case _:
                    raise ValueError('unknown traversal')

            while hs:
                h, p, sigmas = pop()
                h = h()

                if h.is_terminal():
                    yield tuple(sigmas), p * np.array(h.returns())
                elif (i := h.current_player()) < 0:
                    for a, p_prime in h.chance_outcomes():
                        if p_prime or not prune:
                            hs.append(
                                (partial(h.child, a), p_prime * p, sigmas),
                            )
                else:
                    j = h.information_state_string()
                    A = h.legal_actions()
                    A_j = [Sigmas[i][j, a] for a in A]

                    assert 0 != len(A) == len(A_j)

                    for a, a_j in zip(A, A_j):
                        sigma_primes = sigmas.copy()
                        sigma_primes[i] = a_j

                        hs.append((partial(h.child, a), p, sigma_primes))

    write_efg(p_js, A_js, U(), stdout)

    if interp_path is not None:
        with open(interp_path, 'w') as file:
            write_efg_interp(interps, file)


def main():
    args = parse_args()
    gamma = load_game(args.name)

    if gamma.get_type().information == GameType.Information.ONE_SHOT:
        gamma = load_tensor_game(args.name)

        main_nfg(gamma, args.interp_path)
    elif args.stream:
        main_efg2(gamma, args.interp_path, args.prune, args.traversal)
    else:
        main_efg(gamma, args.interp_path, args.prune, args.traversal)


if __name__ == '__main__':
    main()
