#!/usr/bin/env python3

from gurobipy import Env, GRB, Model
import numpy as np


def main():
    header = input().split()

    if header[:2] != ['p', 'nfg']:
        raise ValueError('not UOFTCPRG NFG')

    n, R, C = map(int, header[2:])

    if n != 2:
        raise ValueError('not 2p')

    A = np.empty((R, C))

    for r in range(R):
        for c in range(C):
            u1, u2 = map(float, input().split())

            if not np.isclose(u1 + u2, 0):
                raise ValueError('not 0s')

            A[r, c] = u1

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
