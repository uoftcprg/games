from jsonlines import Writer
from tqdm import tqdm, trange


def save_nfg(U, file):
    assert U.ndim == U.shape[0] + 1

    print('p', 'nfg', *U.shape, file=file)

    for us in U.reshape(U.shape[0], -1).T:
        print(*us, file=file)


def save_nfg_interp(interps, file):
    writer = Writer(file)

    for interp in tqdm(interps):
        writer.write(interp)


def save_efg(p_js, A_js, U, file):
    tokens = ['p', 'efg']

    tokens.append(len(p_js))

    for i in trange(len(p_js)):
        tokens.append(len(p_js[i]))
        tokens.append(max(map(max, A_js[i].values())))

    tokens.append(len(U))

    print(*tokens, file=file)

    for i in trange(len(p_js)):
        for j in tqdm(p_js[i], leave=False):
            tokens = [p_js[i][j]]

            for a in A_js[i][j]:
                tokens.append(a)

            tokens.append(0)

            print(*tokens, file=file)

    for sigmas, us in tqdm(U.items(), total=len(U)):
        print(*sigmas, *us, file=file)


def save_efg_interp(interps, file):
    writer = Writer(file)

    for interp in tqdm(interps):
        for j, A_j in tqdm(interp.items(), leave=False):
            writer.write({'decision_point': j, 'actions': A_j})
