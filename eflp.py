#!/usr/bin/env python3

from argparse import ArgumentParser
from pathlib import Path
from sys import stdin

from gurobipy import Env, GRB, Model
from scipy.sparse import lil_array, load_npz
import numpy as np


def parse_args():
    parser = ArgumentParser(
        usage='%(prog)s [-h] [--atol ATOL] [efg | sfps us]',
    )

    parser.add_argument('files', nargs='*', type=Path)
    parser.add_argument('--atol', default=1e-08, type=float)

    return parser.parse_args()


def load_efg(file, atol):
    header = file.readline().split()

    if header[:2] != ['p', 'efg']:
        raise ValueError('not UOFTCPRG EFG')

    n = int(header[2])

    if n != 2:
        raise ValueError('not 2p')

    J1, Sigma1, J2, Sigma2, U = map(int, header[3:])
    F = lil_array((J1 + 1, Sigma1 + 1))
    f = np.zeros(J1 + 1)
    F[0, 0] = 1
    f[0] = 1

    for j in range(1, J1 + 1):
        p_j, *A_j, eol = map(int, file.readline().split())

        if eol != 0:
            raise ValueError('no EOL')

        F[j, p_j] = -1
        F[j, A_j] = 1

    G = lil_array((J2 + 1, Sigma2 + 1))
    g = np.zeros(J2 + 1)
    G[0, 0] = 1
    g[0] = 1

    for j in range(1, J2 + 1):
        p_j, *A_j, eol = map(int, file.readline().split())

        if eol != 0:
            raise ValueError('no EOL')

        G[j, p_j] = -1
        G[j, A_j] = 1

    A = lil_array((Sigma1 + 1, Sigma2 + 1))

    for _ in range(U):
        tokens = file.readline().split()
        r, c = map(int, tokens[:2])
        u1, u2 = map(float, tokens[2:])

        if abs(u1 + u2) > atol:
            raise ValueError('not 0s')

        A[r, c] += u1

    F = F.tocsr()
    G = G.tocsr()
    A = A.tocsr()

    return F, f, G, g, A


def load_2p0s_efg_npz(sfps, us):
    p_js1, sigmas1, p_js2, sigmas2 = np.load(sfps).values()
    F = lil_array((p_js1.size, sigmas1.size))
    f = np.zeros(p_js1.size)
    F[np.arange(p_js1.size), p_js1] = -1
    indices = np.flatnonzero(sigmas1)
    F[sigmas1[indices], indices] = 1
    F[0, 0] = 1
    f[0] = 1
    G = lil_array((p_js2.size, sigmas2.size))
    g = np.zeros(p_js2.size)
    G[np.arange(p_js2.size), p_js2] = -1
    indices = np.flatnonzero(sigmas2)
    G[sigmas2[indices], indices] = 1
    G[0, 0] = 1
    g[0] = 1
    A = load_npz(us)
    F = F.tocsr()
    G = G.tocsr()
    A = A.tocsr()

    return F, f, G, g, A


def main():
    args = parse_args()

    match args.files:
        case ():
            F, f, G, g, A = load_efg(stdin, args.atol)
        case (efg,):
            with open(efg) as file:
                F, f, G, g, A = load_efg(file, args.atol)
        case (sfps, us):
            F, f, G, g, A = load_2p0s_efg_npz(sfps, us)
        case _:
            raise ValueError('bad args')

    with Env(params={'OutputFlag': 0}) as env:
        m = Model(env=env)
        x = m.addMVar(shape=A.shape[0], name='x')
        u = m.addMVar(shape=g.shape, lb=-GRB.INFINITY, name='u')

        m.setObjective(g @ u, GRB.MAXIMIZE)
        m.addConstr(F @ x == f)
        m.addConstr(x @ A >= u @ G)
        m.optimize()

        x = x.X

        m = Model(env=env)
        y = m.addMVar(shape=A.shape[1], name='y')
        v = m.addMVar(shape=f.shape, lb=-GRB.INFINITY, name='v')

        m.setObjective(f @ v, GRB.MINIMIZE)
        m.addConstr(G @ y == g)
        m.addConstr(A @ y <= v @ F)
        m.optimize()

        y = y.X

    print('v', x @ A @ y)
    print('e', 0)
    print('s', *x.tolist())
    print('s', *y.tolist())


if __name__ == '__main__':
    main()
