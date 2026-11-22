#!/usr/bin/env python3

from argparse import ArgumentParser
from collections import defaultdict
from json import loads
from pathlib import Path
from sys import stdout
import gc

from jpype import JClass, startJVM
import numpy as np

from utilities import save_efg, save_efg_interp

DOMAIN = 'cz.agents.gtlibrary.domain.'
CONFIG = 'cz.agents.gtlibrary.nfg.simalphabeta.SimABConfig'


def parse_args():
    parser = ArgumentParser()

    parser.add_argument('name')
    parser.add_argument('interp_path', nargs='?', type=Path)

    return parser.parse_args()


def main():
    args = parse_args()
    info, state, expander, *params = args.name.split()

    gc.disable()
    startJVM()

    info = JClass(DOMAIN + info)

    for param in params:
        name, value = param.split('=')

        try:
            value = loads(value)
        except ValueError:
            pass

        setattr(info, name, value)

    info()

    expander = JClass(DOMAIN + expander)(JClass(CONFIG)())
    n = 2
    Sigmas = [{} for _ in range(n)]
    p_js = [{} for _ in range(n)]
    A_js = [{} for _ in range(n)]
    U = defaultdict(int)
    interps = None if args.interp_path is None else [{} for _ in range(n)]
    hs = [(JClass(DOMAIN + state)(), 1, [0] * n)]

    while hs:
        h, p, sigmas = hs.pop()

        if h.isGameEnd():
            U[tuple(sigmas)] += p * np.array(h.getUtilities()[:n])
        elif h.isPlayerToMoveNature():
            for a in expander.getActions(h):
                p_prime = h.getProbabilityOfNatureFor(a)

                hs.append((h.performAction(a), p_prime * p, sigmas))
        else:
            i = h.getPlayerToMove().getId()
            j = sigmas[i], h.getISKeyForPlayerToMove().getHash()
            A = list(expander.getActions(h))
            A_j = [
                Sigmas[i].setdefault((j, a.hashCode()), len(Sigmas[i]) + 1)
                for a in A
            ]

            assert 0 != len(A) == len(A_j)

            p_js[i].setdefault(j, sigmas[i])
            A_js[i].setdefault(j, A_j)

            if args.interp_path is not None:
                interps[i].setdefault(j, list(map(str, A)))

            for a, a_j in zip(A, A_j):
                sigma_primes = sigmas.copy()
                sigma_primes[i] = a_j

                hs.append((h.performAction(a), p, sigma_primes))

    save_efg(p_js, A_js, U, stdout)

    if args.interp_path is not None:
        args.interp_path.parent.mkdir(parents=True, exist_ok=True)

        with open(args.interp_path, 'w') as file:
            save_efg_interp(interps, file)


if __name__ == '__main__':
    main()
