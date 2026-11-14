#!/usr/bin/env python3

from argparse import ArgumentParser, BooleanOptionalAction
from pathlib import Path

from scipy.sparse import coo_array, save_npz
from tqdm import trange
import numpy as np


def parse_args():
    parser = ArgumentParser()

    parser.add_argument('sfps', type=Path)
    parser.add_argument('us', type=Path)
    parser.add_argument('--dtype', default='double')
    parser.add_argument('--itype', default='intc')
    parser.add_argument('--atol', default=1e-08, type=float)
    parser.add_argument('--clean', action=BooleanOptionalAction, default=True)

    return parser.parse_args()


def load_sfp(J, Sigma, itype):
    p_js = np.zeros(J + 1, itype)
    sigmas = np.zeros(Sigma + 1, itype)

    for j in trange(1, J + 1):
        p_j, *A_j, eol = map(int, input().split())

        if eol != 0:
            raise ValueError('no EOL')
        elif np.any(sigmas[A_j]):
            raise ValueError('bad sequences')

        p_js[j] = p_j
        sigmas[A_j] = j

    return p_js, sigmas


def load_us(Sigma1, Sigma2, U, dtype, itype, atol, clean):
    data = np.empty(U, dtype)
    rows = np.empty(U, itype)
    cols = np.empty(U, itype)

    for i in trange(U):
        tokens = input().split()
        r, c = map(int, tokens[:2])
        u1, u2 = map(float, tokens[2:])

        if abs(u1 + u2) > atol:
            raise ValueError('not 0s')

        data[i] = u1
        rows[i] = r
        cols[i] = c

    us = coo_array((data, (rows, cols)), (Sigma1 + 1, Sigma2 + 1))

    if clean:
        us.sum_duplicates()
        us.eliminate_zeros()

    return us


def main():
    args = parse_args()
    header = input().split()

    if header[:2] != ['p', 'efg']:
        raise ValueError('not UOFTCPRG EFG')

    n = int(header[2])

    if n != 2:
        raise ValueError('not 2p')

    J1, Sigma1, J2, Sigma2, U = map(int, header[3:])
    p_js1, sigmas1 = load_sfp(J1, Sigma1, args.itype)
    p_js2, sigmas2 = load_sfp(J2, Sigma2, args.itype)
    us = load_us(
        Sigma1,
        Sigma2,
        U,
        args.dtype,
        args.itype,
        args.atol,
        args.clean,
    )

    args.sfps.parent.mkdir(parents=True, exist_ok=True)
    args.us.parent.mkdir(parents=True, exist_ok=True)
    np.savez_compressed(args.sfps, p_js1, sigmas1, p_js2, sigmas2)
    save_npz(args.us, us)


if __name__ == '__main__':
    main()
