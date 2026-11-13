#!/usr/bin/env python3

from argparse import ArgumentParser
from pathlib import Path

import numpy as np


def parse_args():
    parser = ArgumentParser()

    parser.add_argument('npz', type=Path)
    parser.add_argument('--dtype', default='double')
    parser.add_argument('--atol', default=1e-08, type=float)

    return parser.parse_args()


def main():
    args = parse_args()
    header = input().split()

    if header[:2] != ['p', 'nfg']:
        raise ValueError('not UOFTCPRG NFG')

    n = int(header[2])

    if n != 2:
        raise ValueError('not 2p')

    R, C = map(int, header[3:])
    A = np.empty((R, C), args.dtype)

    for r in range(R):
        for c in range(C):
            u1, u2 = map(float, input().split())

            if abs(u1 + u2) > args.atol:
                raise ValueError('not 0s')

            A[r, c] = u1

    args.npz.parent.mkdir(parents=True, exist_ok=True)
    np.savez_compressed(args.npz, A)


if __name__ == '__main__':
    main()
