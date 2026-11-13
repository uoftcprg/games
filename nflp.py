#!/usr/bin/env python3

from argparse import ArgumentParser
from pathlib import Path
from sys import stdin

from gurobipy import Env, GRB, Model
import numpy as np


def parse_args():
    parser = ArgumentParser(usage='%(prog)s [-h] [--atol ATOL] [nfg | npz]')

    parser.add_argument('file', nargs='?', type=Path)
    parser.add_argument('--atol', default=1e-08, type=float)

    return parser.parse_args()


def load_nfg(file, atol):
    header = file.readline().split()

    if header[:2] != ['p', 'nfg']:
        raise ValueError('not UOFTCPRG NFG')

    n = int(header[2])

    if n != 2:
        raise ValueError('not 2p')

    R, C = map(int, header[3:])
    A = np.empty((R, C))

    for r in range(R):
        for c in range(C):
            u1, u2 = map(float, file.readline().split())

            if abs(u1 + u2) > atol:
                raise ValueError('not 0s')

            A[r, c] = u1

    return A


def main():
    args = parse_args()

    if args.file is None:
        A = load_nfg(stdin, args.atol)
    else:
        try:
            (A,) = np.load(args.file).values()
        except ValueError:
            with open(args.file) as file:
                A = load_nfg(file, args.atol)

    with Env(params={'OutputFlag': 0}) as env:
        m = Model(env=env)
        x = m.addMVar(shape=A.shape[0], name='x')
        u = m.addVar(lb=-GRB.INFINITY, name='u')

        m.setObjective(u, GRB.MAXIMIZE)
        m.addConstr(x.sum() == 1)
        m.addConstr(x @ A >= u)
        m.optimize()

        x = x.X

        m = Model(env=env)
        y = m.addMVar(shape=A.shape[1], name='y')
        v = m.addVar(lb=-GRB.INFINITY, name='v')

        m.setObjective(v, GRB.MINIMIZE)
        m.addConstr(y.sum() == 1)
        m.addConstr(A @ y <= v)
        m.optimize()

        y = y.X

    print('v', x @ A @ y)
    print('e', 0)
    print('s', *x.tolist())
    print('s', *y.tolist())


if __name__ == '__main__':
    main()
