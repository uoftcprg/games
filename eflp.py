#!/usr/bin/env python3

from gurobipy import Env, GRB, Model
from scipy.sparse import lil_array
import numpy as np


def main():
    header = input().split()

    if header[:2] != ['p', 'efg']:
        raise ValueError('not UOFTCPRG EFG')

    n, J1, Sigma1, J2, Sigma2, U = map(int, header[2:])

    if n != 2:
        raise ValueError('not 2p')

    F = lil_array((J1 + 1, Sigma1 + 1))
    f = np.zeros(J1 + 1)
    F[0, 0] = 1
    f[0] = 1

    for j in range(1, J1 + 1):
        p_j, *A_j, eol = map(int, input().split())

        if eol != 0:
            raise ValueError('no EOL')

        F[j, p_j] = -1
        F[j, A_j] = 1

    G = lil_array((J2 + 1, Sigma2 + 1))
    g = np.zeros(J2 + 1)
    G[0, 0] = 1
    g[0] = 1

    for j in range(1, J2 + 1):
        p_j, *A_j, eol = map(int, input().split())

        if eol != 0:
            raise ValueError('no EOL')

        G[j, p_j] = -1
        G[j, A_j] = 1

    A = lil_array((Sigma1 + 1, Sigma2 + 1))

    for _ in range(U):
        tokens = input().split()
        r, c = map(int, tokens[:2])
        u1, u2 = map(float, tokens[2:])

        if not np.isclose(u1 + u2, 0):
            raise ValueError('not 0s')

        A[r, c] += u1

    F = F.tocsr()
    G = G.tocsr()
    A = A.tocsr()

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
