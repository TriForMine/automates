#######################################################
#  Automates & Langages  -  L3 I / MI / ST  - 2023/24 #
#  TP 3  - Algorithmes de recherche de motif - II     #
#######################################################


print('------------------------------------ TP 3 ---------------------------------------------')

#  Algorithme de Boyer Moore
############################


print('### Exercice 1 ###')


def dicoDerOcc(motif):  # retourne le dictionnaire des dernières occurrences
    dico = {}

    for i in range(len(motif)):
        dico[motif[i]] = i

    return dico


print(dicoDerOcc('abracadabra'))

print('### Exercice 2 ###')


def rechercheBMH(motif, texte):  # version simplifiée de BM -> BM Horspool

    dico = dicoDerOcc(motif)
    lm = len(motif)
    lt = len(texte)
    i = lm - 1  # indice motif
    j = lm - 1  # indice texte

    while j < lt:
        if motif[i] == texte[j]:
            if i == 0:
                return j
            else:
                i -= 1
                j -= 1
        else:
            d = dico.get(texte[j], -1)

            j += lm - min(i, d + 1)
            i = lm - 1

    return -1


def RechercheBMH(fichier, motif):
    f_in = open(fichier, 'r', encoding='utf-8')
    texte = f_in.read()
    f_in.close()

    position = rechercheBMH(motif, texte)
    if position == -1:
        print('Le motif', motif, 'n''apparaît pas dans le fichier', fichier)
    else:
        print('Le motif', motif, 'apparaît en position', position, 'dans le fichier', fichier)


RechercheBMH('horla.txt', 'Rouen')

#   Algorithme de Rabin-Karp
#############################


print('### Exercice 3.1 ###')


def str2int(s):
    return sum(ord(s[-i]) * 256 ** (i - 1) for i in range(1, len(s) + 1))


# This is a base 16 conversion
def str2int_bis(s):
    return int(''.join(hex(ord(c))[2:] for c in s), 16)

def hash(s):
    return str2int_bis(s) % 101


print('hash(abracadabra) =', hash('abracadabra'))

# def str2intBIS(s) :


print('### Exercice 3.2 ###')


def rechercheRK(motif, texte):
    hm = hash(motif)
    lm = len(motif)
    lt = len(texte)

    for i in range(lt - lm + 1):
        if hm == hash(texte[i:i + lm]) and motif == texte[i:i + lm]:
            return i

    return -1


def RechercheRK(fichier, motif):
    f_in = open(fichier, 'r', encoding='utf-8')
    texte = f_in.read()
    f_in.close()

    position = rechercheRK(motif, texte)
    if position == -1:
        print('RK : Le motif', motif, 'n''apparaît pas dans le fichier', fichier)
    else:
        print('RK : Le motif', motif, 'apparaît en position', position, 'dans le fichier', fichier)


RechercheRK('horla.txt', 'admirable')
RechercheRK('horla.txt', 'Havre')
RechercheRK('horla.txt', 'racine')

print('### Exercice 4 ###')


# calcul amorti de l'empreinte en fonction de celle du facteur précédent
def update(h, n, s_i, s_j):
    h -= (ord(s_i) * (256 ** (n - 1)))
    h = (h * 256)
    h = (h + ord(s_j))
    return h % 101


h = hash('abracadabra')
assert hash('bracadabrab') == update(h, len('abracadabra'), 'a', 'b')


def rechercheRK2(motif, texte):
    hm = hash(motif)
    lm = len(motif)
    lt = len(texte)
    h = hash(texte[:lm])

    for i in range(lt - lm + 1):
        if hm == h and motif == texte[i:i + lm]:
            return i
        if i < lt - lm:
            h = update(h, lm, texte[i], texte[i + lm])

    return -1


def RechercheRK2(fichier, motif):
    f_in = open(fichier, 'r', encoding='utf-8')
    texte = f_in.read()
    f_in.close()

    position = rechercheRK2(motif, texte)
    if position == -1:
        print('RK2 : Le motif', motif, 'n''apparaît pas dans le fichier', fichier)
    else:
        print('RK2 : Le motif', motif, 'apparaît en position', position, 'dans le fichier', fichier)


RechercheRK2('horla.txt', 'admirable')
RechercheRK2('horla.txt', 'Havre')
RechercheRK2('horla.txt', 'racine')
RechercheRK2('horla.txt', 'Rouen')

# Version avec adler32
print('### Adler32 ###')


def adler32(s):
    a, b = 1, 0
    for c in s:
        a = (a + ord(c)) % 65521
        b = (b + a) % 65521
    return (b << 16) | a


print('adler32(abracadabra) =', adler32('abracadabra'))


def update_adler32(h, n, s_i, s_j):
    s1 = h & 0xFFFF
    s2 = h >> 16

    s1 = (s1 - ord(s_i) + ord(s_j)) % 65521
    s2 = (s2 - n * ord(s_i) + s1 - 1) % 65521

    return (s2 << 16) | s1


h = adler32('abracadabra')
assert adler32('bracadabrab') == update_adler32(h, len('abracadabra'), 'a', 'b')


def rechercheRK3(motif, texte):
    hm = adler32(motif)
    lm = len(motif)
    lt = len(texte)
    h = adler32(texte[:lm])

    for i in range(lt - lm + 1):
        if hm == h and motif == texte[i:i + lm]:
            return i
        if i < lt - lm:
            h = update_adler32(h, lm, texte[i], texte[i + lm])

    return -1


def RechercheRK3(fichier, motif):
    f_in = open(fichier, 'r', encoding='utf-8')
    texte = f_in.read()
    f_in.close()

    position = rechercheRK3(motif, texte)
    if position == -1:
        print('RK2 : Le motif', motif, 'n''apparaît pas dans le fichier', fichier)
    else:
        print('RK2 : Le motif', motif, 'apparaît en position', position, 'dans le fichier', fichier)


RechercheRK3('horla.txt', 'admirable')
RechercheRK3('horla.txt', 'Havre')
RechercheRK3('horla.txt', 'racine')
RechercheRK3('horla.txt', 'Rouen')
