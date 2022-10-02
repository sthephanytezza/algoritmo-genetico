import numpy as np
import copy
import random


def different_column_violations(sol):
    conflicts = 0

    for i in range(len(sol)):
        for j in range(len(sol)):
            if i != j and sol[i] == sol[j]:
                conflicts += 1

    return conflicts


def different_diagonal_violations(sol):
    conflicts = 0
    for i in range(len(sol)):
        for j in range(len(sol)):
            deltax = abs(sol[i] - sol[j])
            deltay = abs(i - j)
            if (deltax == deltay).all():
                conflicts += 1

    return conflicts


def obj(sol):
    return different_diagonal_violations(sol) + different_column_violations(sol)


def pop_int(n, k):
    return [np.random.permutation(n) for i in range(k)]


def mutation(sol):
    neighbor = copy.copy(sol)

    idx1 = np.random.randint(0, len(sol))
    idx2 = np.random.randint(0, len(sol))

    neighbor[idx1], neighbor[idx2] = neighbor[idx2], neighbor[idx1]

    return neighbor


def crossover(sol1, sol2):
    mask = np.random.randint(2, size=len(sol1))
    f1 = copy.copy(sol1)
    for i in range(len(sol1)):
        if mask[i] == 0:
            f1[i] = sol2[i]

    f2 = copy.copy(sol2)
    for i in range(len(sol2)):
        if mask[i] == 0:
            f2[i] = sol1[i]

    return f1, f2


def select(sol):
    """
        Realiza a seleção do individuo mais apto por torneio
    """
    best = 0
    best_score = obj(sol[0])
    for i in range(len(sol)):
        score = obj(sol[i])
        if score < best_score:
            best = i
            best_score = score

    return best


if __name__ == '__main__':
    pop = pop_int(10, 8)

    prob_mutation = 0.2
    prob_crossover = 0.7
    generations = 100
    tournamentLen = 50

    indice_pai1 = 0
    indice_pai2 = 0
    indice_melhor = 0
    score_melhor = 0

    filho = []
    f1 = []
    f2 = []

    for i in range(generations):
        for j in range(tournamentLen):
            prob = random.random()
            if prob < prob_crossover:
                indice_pai1 = random.randint(0, len(pop)-1)
                while True:
                    indice_pai2 = random.randint(0, len(pop)-1)
                    if indice_pai1 != indice_pai2:
                        break
                f1, f2 = crossover(pop[indice_pai1], pop[indice_pai2])
                filho.append(f1)
                filho.append(f2)
                prob = random.random()
                if prob < prob_mutation:
                    mutation(filho)

                score_pai1 = obj(pop[indice_pai1])
                score_filho = obj(filho[select(filho)])

                if score_filho < score_pai1:
                    pop[indice_pai1] = filho[select(filho)]

                filho.clear()

        indice_melhor = select(pop)
        score_melhor = obj(pop[indice_melhor])

    print("indice", indice_melhor)
    print("score", score_melhor)
    print("pop", pop[indice_melhor])
