#!/usr/bin/env python3

from argparse import ArgumentParser
from collections import defaultdict
from pathlib import Path
from sys import stdin, stdout

import numpy as np

from utilities import save_efg, save_efg_interp


def parse_args():
    parser = ArgumentParser()

    parser.add_argument('interp_path', nargs='?', type=Path)

    return parser.parse_args()


def main():
    args = parse_args()
    nodes = {}
    infosets = {}

    for line in stdin:
        match line.split():
            case ['node', h, *tokens]:
                nodes[h] = tokens
            case ['infoset', j, 'nodes', *hs]:
                for h in hs:
                    infosets[h] = j

    n = max(int(t[1]) for t in nodes.values() if t[0] == 'player')
    Sigmas = [{} for _ in range(n)]
    p_js = [{} for _ in range(n)]
    A_js = [{} for _ in range(n)]
    U = defaultdict(int)
    interps = None if args.interp_path is None else [{} for _ in range(n)]
    hs = [('/', 1, [0] * n)]

    while hs:
        h, p, sigmas = hs.pop()

        match nodes[h]:
            case ['leaf', 'payoffs', *us]:
                us = [float(u.split('=')[1]) for u in us]

                assert len(us) == n

                U[tuple(sigmas)] += p * np.array(us)
            case ['chance', 'actions', *A]:
                A, ps = zip(*(a.rsplit('=', 1) for a in A))
                ps = np.array(ps, float)

                for a, p_prime in zip(A, ps / ps.sum()):
                    hs.append((f'{h.rstrip("/")}/C:{a}', p_prime * p, sigmas))
            case ['player', i, 'actions', *A]:
                h_prime = f'{h.rstrip("/")}/P{i}:'
                i = int(i) - 1
                j = infosets.get(h, h)
                A_j = [
                    Sigmas[i].setdefault((j, a), len(Sigmas[i]) + 1)
                    for a in A
                ]

                assert 0 != len(A) == len(A_j)

                p_js[i].setdefault(j, sigmas[i])
                A_js[i].setdefault(j, A_j)

                if args.interp_path is not None:
                    interps[i].setdefault(j, A)

                for a, a_j in zip(A, A_j):
                    sigma_primes = sigmas.copy()
                    sigma_primes[i] = a_j

                    hs.append((h_prime + a, p, sigma_primes))

    save_efg(p_js, A_js, U, stdout)

    if args.interp_path is not None:
        args.interp_path.parent.mkdir(parents=True, exist_ok=True)

        with open(args.interp_path, 'w') as file:
            save_efg_interp(interps, file)


if __name__ == '__main__':
    main()
