from typing import Tuple, List
from numpy import *


def drawpath(x: str, y: str, path: List[Tuple[str, str]]) -> str:
    res = ""
    i = 0
    j = 0

    arr = full((len(x) + 1, len(y) + 1), " ")

    for i in range(len(x) + 1):
        arr[i, 0] = x[i - 1] if i > 0 else " "

    for j in range(len(y) + 1):
        arr[0, j] = y[j - 1] if j > 0 else " "

    prev = (len(x) + 1, len(y) + 1)
    for (a, b, i, j) in reversed(path):
        if i == prev[0] and j == prev[1]:
            arr[i, j] = " "
        elif i == prev[0]:
            arr[i, j] = "→"
        elif j == prev[1]:
            arr[i, j] = "↓"
        else:
            arr[i, j] = "↘"
        prev = (i, j)

    for i in range(len(x) + 1):
        for j in range(len(y) + 1):
            res += "{:<2}".format(arr[i, j])
        if i < len(x):
            res += "\n"

    return res

def alignment(x: str, y: str, path: List[Tuple[str, str]]) -> str:
    # Print on two lines the alignment of x and y
    # according to the path
    # If we have a gap, we print a red dash if it is in x, a green dash if it is in y
    # And the one that changes is in blue

    res = ""

    for (a, b, i, j) in path:
        if a == "-":
            res += "\033[32m" + b + "\033[0m"
        elif b == "-":
            res += "\033[31m-\033[0m"
        elif x[i] != y[j]:
            res += "\033[34m" + a + "\033[0m"
        else:
            res += a

    res += "\n"

    for (a, b, i, j) in path:
        if b == "-":
            res += "\033[32m-\033[0m"
        elif a == "-":
            res += "\033[31m-\033[0m"
        elif x[i] != y[j]:
            res += "\033[34m" + b + "\033[0m"
        else:
            res += b

    return res

def table(x: str, y: str):
    res = zeros((len(x) + 1, len(y) + 1), dtype=int)
    res[1:, 0] = arange(1, len(x) + 1)
    res[0, 1:] = arange(1, len(y) + 1)

    for i in range(1, len(x) + 1):
        for j in range(1, len(y) + 1):
            res[i, j] = min(array([res[i - 1, j] + 1, res[i, j - 1] + 1, res[i - 1, j - 1] + (x[i - 1] != y[j - 1])]))

    return res


print("Exercice 1.2")
print(table("rame", "marin"))

print("--------------------")


def distance(x: str, y: str):
    return table(x, y)[-1, -1]


print("Exercice 1.3")

print("distance('rame', 'marin') =", distance("rame", "marin"))
print("distance('rame', 'rame') =", distance("rame", "rame"))
print("distance('rame', 'ramee') =", distance("rame", "ramee"))
print("distance('rame', 'rome') =", distance("rame", "rome"))

print("--------------------")


def chemin(x: str, y: str):
    tab = table(x, y)
    i = len(x)
    j = len(y)
    res = []

    while i > 0 or j > 0:
        if i > 0 and j > 0:
            if tab[i, j] == tab[i - 1, j - 1] + (x[i - 1] != y[j - 1]):
                i -= 1
                j -= 1
                res.append((x[i], y[j], i, j))
            elif tab[i, j] == tab[i - 1, j] + 1:
                i -= 1
                res.append((x[i], "-", i, j))
            elif tab[i, j] == tab[i, j - 1] + 1:
                j -= 1
                res.append(("-", y[j], i, j))
        elif i > 0:
            i -= 1
            res.append((x[i], "-", i, j))
        elif j > 0:
            j -= 1
            res.append(("-", y[j], i, j))

    return res[::-1]


print("Exercice 2.")
path = chemin("rame", "marin")
print(drawpath("rame", "marin", path))
print(alignment("rame", "marin", path))

print("--------------------")


def parcours(x: str, y: str, tab: list, i: int, j: int):
    if i == 0 and j == 0:
        return [[]]

    results = []

    if i > 0 and tab[i, j] == tab[i - 1, j] + 1:
        for r in parcours(x, y, tab, i - 1, j):
            results.append([(x[i - 1], "-", i - 1, j)] + r)

    if j > 0 and tab[i, j] == tab[i, j - 1] + 1:
        for r in parcours(x, y, tab, i, j - 1):
            results.append([("-", y[j - 1], i, j - 1)] + r)

    if i > 0 and j > 0 and tab[i, j] == tab[i - 1, j - 1] + (x[i - 1] != y[j - 1]):
        for r in parcours(x, y, tab, i - 1, j - 1):
            results.append([(x[i - 1], y[j - 1], i - 1, j - 1)] + r)

    return results


def tousChemins(x: str, y: str):
    tab = table(x, y)
    i = len(x)
    j = len(y)

    res = parcours(x, y, tab, i, j)

    for i in range(len(res)):
        res[i] = res[i][::-1]

    return res


print("Exercice 3.")

for chemin in tousChemins("rame", "marin"):
    print(drawpath("rame", "marin", chemin))
    print(alignment("rame", "marin", chemin))

for chemin in tousChemins("voilier", "olivier"):
    print(drawpath("voilier", "olivier", chemin))
    print(alignment("voilier", "olivier", chemin))