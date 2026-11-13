#!/usr/bin/env python3

from collections import defaultdict
from sys import stdout

import numpy as np

from utilities import write_efg


def load_sfp(J, Sigma):
    firsts = list(map(int, input().split()))
    lasts = list(map(int, input().split()))
    parents = list(map(int, input().split()))

    if not len(firsts) == len(lasts) == len(parents) == J:
        raise ValueError('bad decision points')

    p_js = {}
    A_js = {}
    sigma = 0

    for j in reversed(range(J)):
        p_j = Sigma - parents[j]
        A_j = list(range(Sigma - lasts[j], Sigma - firsts[j] + 1))

        if not A_j or not 0 <= p_j <= sigma == A_j[0] - 1:
            raise ValueError('bad sequences')

        p_js[j] = p_j
        A_js[j] = A_j
        sigma = A_j[-1]

    if sigma != Sigma:
        raise ValueError('bad sequences')

    return p_js, A_js


def load_us(Sigma1, Sigma2):
    indptr = list(map(int, input().split()))
    indices = list(map(int, input().split()))
    data = list(map(float, input().split()))

    if (
            len(indptr) != Sigma1 + 2
            or indptr != sorted(indptr)
            or indptr[0] != 0
            or not indptr[-1] == len(indices) == len(data)
    ):
        raise ValueError('bad payoffs')

    U = defaultdict(int)

    for r, (start, stop) in enumerate(zip(indptr, indptr[1:])):
        for c, u in zip(indices[start:stop], data[start:stop]):
            if not 0 <= c <= Sigma2:
                raise ValueError('bad payoffs')

            U[Sigma1 - r, Sigma2 - c] += np.array((u, -u))

    return U


def main():
    header = input().split()

    if header != ['CONSTANT_SUM', '0']:
        raise ValueError('not 0s')

    J1, Sigma1, _, J2, Sigma2, _ = map(int, input().split())
    Sigma1 -= 1
    Sigma2 -= 1
    p_js1, A_js1 = load_sfp(J1, Sigma1)
    p_js2, A_js2 = load_sfp(J2, Sigma2)
    U = load_us(Sigma1, Sigma2)

    write_efg((p_js1, p_js2), (A_js1, A_js2), U, stdout)


if __name__ == '__main__':
    main()
