#######################################################
#  Automates & Langages  -  L3 I / MI / ST  - 2023/24 #
#  TP 2  - Algorithmes de recherche de motif - I      #                                    
#######################################################


print('------------------------------------ TP 2 ---------------------------------------------')


#  jeu de 95 caractères Unicode latin de base (hors commandes)

# for i in range(95) :
#     print(hex(i+32),' : ',chr(i+32))
#     
# print()


# pour visualiser la lettre i d'une chaîne

def marque(chaineCar, i):
    return '{}[{}]{}'.format(chaineCar[:i], chaineCar[i], chaineCar[i + 1:])


print(marque('blabla', 2))
print()


# pour visualiser la comparaison entre la lettre i du motif et la lettre i+j du texte

def compare(motif, texte, i, j):
    print('{}\n{}{}\n'.format(marque(texte, j), ' ' * j, marque(motif, i)))


compare('blabla', 'lalablablère', 5, 4)


def comparePlus(motif, texte, i, j):
    if texte[j] != motif[i]:
        print('{} : ! \n{}{}\n'.format(marque(texte, j), ' ' * j, marque(motif, i)))
    else:
        print('{}\n{}{}\n'.format(marque(texte, j), ' ' * j, marque(motif, i)))


comparePlus('blabla', 'lalablablère', 5, 4)

#  Algorithme de recherche naif
###############################

print('### Exercice 1 ###')


def recherche(motif, texte):
    lm = len(motif)
    lt = len(texte)

    # Pire des cas O(m*n)
    for i in range(lt - lm + 1):
        j = 0
        while j < lm and texte[i + j] == motif[j]:
            j = j + 1
        if j == lm:
            return i
    return -1


f_in = open('testMurmure.txt', 'r', encoding='utf-8')
texte = f_in.read()
f_in.close()

print('murmure est en position', recherche('murmure', texte), 'dans le texte.')
print('azeaze est en position', recherche('azeaze', texte), 'dans le texte.')

#  Algorithme de Knuth-Morris-Pratt
###################################


print('### Exercice 2 ###')


def table(motif):  # table[i] = longueur du plus long suffixe de motif[i] aussi préfixe du motif
    lm = len(motif)
    T = [0] * lm
    i = -1
    T[0] = i
    for j in range(1, lm):
        while (i != -1) and (motif[i] != motif[j - 1]):
            i = T[i]
        i = i + 1
        T[j] = i
    return T


print(table('blalablalablabla'))
print(table('murmure'))

print('### Exercice 3 ###')


def rechercheMP(motif, texte):  # utilise table(motif) pour se relancer suite à un échec
    T = table(motif)
    lm = len(motif)
    lt = len(texte)
    i = 0  # indice motif
    j = 0  # indice texte
    while j < lt and i < lm:
        if texte[j] == motif[i]:
            i = i + 1
            j = j + 1
        elif i == 0:
            j = j + 1
        else:
            i = T[i]

    if i == lm:
        return j - lm
    else:
        return -1


def RechercheMP(fichier, motif):
    f_in = open(fichier, 'r', encoding='utf-8')
    texte = f_in.read()
    f_in.close()
    position = rechercheMP(motif, texte)
    if position == -1:
        print('Recherche MP : Le motif', motif, 'n''apparaît pas dans le fichier.', fichier)
    else:
        print('Recherche MP : Le motif', motif, 'apparaît en position', position, 'dans le fichier :', fichier)


RechercheMP('testMurmure.txt', 'murmure')
RechercheMP('horla.txt', 'Havre')
RechercheMP('horla.txt', 'AZEZAE')

# sans redondance dans le motif, KMP perd de son intérêt ... Imaginons son exécution sur du binaire plutôt !


print('### Exercice 4 ###')


def rechercheKMP(motif, texte, printCompare):
    T = table(motif)
    lm = len(motif)
    lt = len(texte)
    i = 0  # indice motif
    j = 0  # indice texte
    while j < lt and i < lm:
        if printCompare:
            comparePlus(motif, texte, i, j)
        if texte[j] == motif[i]:
            i = i + 1
            j = j + 1
        elif i == 0:
            j = j + 1
        else:
            i = T[i]

    if i == lm:
        return j - lm
    else:
        return -1


def RechercheKMP(fichier, motif):
    f_in = open(fichier, 'r', encoding='utf-8')
    texte = f_in.read()
    f_in.close()

    position = rechercheKMP(motif, texte, False)
    if position == -1:
        print('Recherche KMP : Le motif', motif, 'n''apparaît pas dans le fichier.', fichier)
    else:
        print('Recherche KMP : Le motif', motif, 'apparaît en position', position, 'dans le fichier.', fichier)


print(rechercheKMP('murmure', 'les murs de mures murmurent', True))
RechercheKMP('testMurmure.txt', 'murmure')
RechercheKMP('horla.txt', 'Havre')

#  Algorithme de Aho-Corasick
#############################


print('### Exercice 5 ###')


def construireAutomate(motif, A):
    etatInitial = 0
    terminal = etatInitial
    delta = {}

    for b in A:
        delta[(etatInitial, b)] = etatInitial

    for a in motif:
        temp = delta.get((terminal, a), -1)
        delta[(terminal, a)] = terminal + 1
        for b in A:
            delta[(terminal + 1, b)] = delta.get((temp, b), -1)
        terminal = terminal + 1
    return delta


def setEtat(delta, etat, a, val):
    delta[etat][a] = val


def getEtat(delta, etat, a):
    return delta[etat].get(a, -1)


def construireAutomate2(motif, A):
    etatInitial = 0
    terminal = etatInitial
    delta = [{} for i in range(len(motif) + 1)]

    for b in A:
        setEtat(delta, etatInitial, b, etatInitial)

    for a in motif:
        temp = getEtat(delta, terminal, a)
        setEtat(delta, terminal, a, terminal + 1)
        for b in A:
            setEtat(delta, terminal + 1, b, getEtat(delta, temp, b))
        terminal = terminal + 1

    return delta


# print(construireAutomate('2023', ['0', '2', '3']))
print(construireAutomate2('2023', ['0', '2', '3']))


def RechercheAC(fichier, motif):
    f_in = open(fichier, 'r', encoding='utf-8')
    texte = f_in.read()
    f_in.close()

    A = set(texte)

    automate = construireAutomate2(motif, A)

    etat = 0
    for i in range(len(texte)):
        etat = getEtat(automate, etat, texte[i])
        if etat == len(motif):
            print('Recherche AC : Le motif', motif, 'apparaît en position', i - len(motif) + 1, 'dans le fichier :',
                  fichier)
            return

    print('Recherche AC : Le motif', motif, 'n''apparaît pas dans le fichier.', fichier)


RechercheAC('testMurmure.txt', 'murmure')
RechercheAC('horla.txt', 'Havre')
RechercheAC('horla.txt', 'AZEZAE')

import graphviz


def dessinerAutomate(delta, A):
    g = graphviz.Digraph(format='png')
    g.attr(rankdir='LR')
    g.node(str(0), shape='circle')
    g.attr('node', shape='doublecircle')
    g.node(str(len(delta) - 1))
    g.attr('node', shape='circle')
    for etat in range(len(delta)):
        for a in A:
            if getEtat(delta, etat, a) != -1:
                g.edge(str(etat), str(getEtat(delta, etat, a)), label=a)
    g.render(view=True)


dessinerAutomate(construireAutomate2('2023', ['0', '2', '3']), ['0', '2', '3'])
