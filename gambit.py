#!/usr/bin/env python3

from argparse import ArgumentParser
from collections import defaultdict
from pathlib import Path
from sys import stdout

import numpy as np
import pygambit as gbt

from utilities import save_efg, save_efg_interp, save_nfg, save_nfg_interp


def parse_args():
    parser = ArgumentParser()

    parser.add_argument('name')
    parser.add_argument('interp_path', nargs='?', type=Path)

    return parser.parse_args()


def main_nfg(gamma, interp_path):
    U = np.array(gamma.to_arrays(float), float)

    save_nfg(U, stdout)

    if interp_path is not None:
        interps = [[s.label for s in i.strategies] for i in gamma.players]

        interp_path.parent.mkdir(parents=True, exist_ok=True)

        with open(interp_path, 'w') as file:
            save_nfg_interp(interps, file)


def main_efg(gamma, interp_path):
    assert gamma.is_perfect_recall

    n = len(gamma.players)
    Sigmas = [{} for _ in range(n)]
    p_js = [{} for _ in range(n)]
    A_js = [{} for _ in range(n)]
    U = defaultdict(int)
    interps = None if interp_path is None else [{} for _ in range(n)]
    hs = [(gamma.root, 1, [0] * n, np.zeros(n))]

    while hs:
        h, p, sigmas, us = hs.pop()

        if h.outcome:
            us = us + [float(h.outcome[i]) for i in gamma.players]

        if h.is_terminal:
            U[tuple(sigmas)] += p * us
        elif h.player.is_chance:
            for a, h_prime in zip(h.infoset.actions, h.children):
                hs.append((h_prime, float(a.prob) * p, sigmas, us))
        else:
            i = h.player.number
            j = h.infoset.number
            A = list(h.infoset.actions)
            A_j = [Sigmas[i].setdefault((j, a), len(Sigmas[i]) + 1) for a in A]

            assert 0 != len(A) == len(A_j)

            p_js[i].setdefault(j, sigmas[i])
            A_js[i].setdefault(j, A_j)

            if interp_path is not None:
                interps[i].setdefault(j, [a.label for a in A])

            for a_j, h_prime in zip(A_j, h.children):
                sigma_primes = sigmas.copy()
                sigma_primes[i] = a_j

                hs.append((h_prime, p, sigma_primes, us))

    save_efg(p_js, A_js, U, stdout)

    if interp_path is not None:
        interp_path.parent.mkdir(parents=True, exist_ok=True)

        with open(interp_path, 'w') as file:
            save_efg_interp(interps, file)


def main():
    args = parse_args()
    gamma = gbt.catalog.load(args.name)

    if gamma.is_tree:
        main_efg(gamma, args.interp_path)
    else:
        main_nfg(gamma, args.interp_path)


if __name__ == '__main__':
    main()
