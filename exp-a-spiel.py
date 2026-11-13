#!/usr/bin/env python3

from argparse import ArgumentParser
from dataclasses import dataclass
from pathlib import Path

from tqdm import trange
import numpy as np
import eas

from utilities import save_efg, save_efg_interp


def parse_args():
    parser = ArgumentParser()

    parser.add_argument('name')
    parser.add_argument('efg_path', type=Path)
    parser.add_argument('interp_path', nargs='?', type=Path)

    return parser.parse_args()


def main():
    args = parse_args()
    traverser = getattr(eas, args.name + 'Traverser')()
    p_js = {}, {}
    A_js = {}, {}
    interps = None if args.interp_path is None else ({}, {})

    for i in trange(2):
        legal_actions = traverser.legal_actions(i)
        parent_sequences = traverser.parent_sequences(i)

        assert legal_actions.shape[0] == parent_sequences.shape[0]

        for r in trange(legal_actions.shape[0], leave=False):
            j = traverser.infoset_desc(i, r)
            A = np.flatnonzero(legal_actions[r])
            p_js[i][j] = parent_sequences[r] + 1
            A_js[i][j] = 9 * r + A + 1

            if args.interp_path is not None:
                interps[i].setdefault(j, A.tolist())

    @dataclass
    class U:
        _nnz: int | None = None

        def __len__(self):
            if self._nnz is None:
                self._nnz = 0

                for t in trange(traverser.NUM_SUBTREES):
                    self._nnz += traverser.utility_matrix_nnz([t])

            return self._nnz

        def items(self):
            for t in range(traverser.NUM_SUBTREES):
                sigmas0, sigmas1, us = traverser.utility_matrix([t])

                for sigma0, sigma1, u in zip(sigmas0, sigmas1, us):
                    yield (sigma0 + 1, sigma1 + 1), (u, -u)

    args.efg_path.parent.mkdir(parents=True, exist_ok=True)

    with open(args.efg_path, 'w') as file:
        save_efg(p_js, A_js, U(), file)

    if args.interp_path is not None:
        args.interp_path.parent.mkdir(parents=True, exist_ok=True)

        with open(args.interp_path, 'w') as file:
            save_efg_interp(interps, file)


if __name__ == '__main__':
    main()
