# LZW

def creeDT(n):
    dictionnaire = [chr(i) for i in range(32, 127)] + [""] * n
    return dictionnaire, 0


def estPlein(dt):
    return len(dt[0]) == dt[1] + 95


def ajoute(dt, ch):
    d, t = dt
    if not estPlein(dt):
        d[t + 95] = ch
        return d, t + 1
    return dt


print("Exercice 1.")

print('Création du dictionnaire')
dt = creeDT(4)
print(dt[0])
print(dt[1])

print("Est plein ?")
print(estPlein(dt))

print('Ajout de "a" à "d"')
dt = ajoute(dt, "a")
dt = ajoute(dt, "b")
dt = ajoute(dt, "c")
dt = ajoute(dt, "d")

print(dt[0])
print(dt[1])

print("Est plein ?")
print(estPlein(dt))

print()
print("--------------------")
print("Exercice 2.")
print()


def encodeLZW(m: str):
    dt = creeDT(5000)
    res = []

    i = 0
    while i < len(m):
        j = 1
        while i + j <= len(m) and m[i:i + j] in dt[0]:
            j += 1
        mot = m[i:i + j - 1]
        res.append(dt[0].index(mot))

        if m[i:i + j] not in dt[0]:
            # Add new word to the dictionary if it doesn't exist
            if mot not in dt[0]:
                dt = ajoute(dt, mot)

        if j == 1:
            break

        i += j - 1

    return res


print("encodeLZW('abracadabra') =", encodeLZW("abracadabra"))
print(len(encodeLZW("abracadabra")))

print()
print('-------------------')
print("Exercice 3.")
print()


def decodeLZW(l: list):
    dt = creeDT(max(l) - 94)
    res = ""

    i = 0
    while i < len(l):
        if l[i] < len(dt[0]):
            m = dt[0][l[i]]
            res += m

            # Add new word to the dictionary if it doesn't exist
            if m not in dt[0]:
                dt = ajoute(dt, m)

            # If there's another character in the index, add it to the word
            if i + 1 < len(l):
                a = dt[0][l[i + 1]]
                if a != "":
                    dt = ajoute(dt, m + a)
        else:
            # Reconstruct the current word from the dictionary
            m = dt[0][l[i]]

            # Check if the current word exists in the dictionary
            if m not in dt[0]:
                # If the current word doesn't exist, try to reconstruct it
                m0 = dt[0][l[i - 1]]
                if m0 != "":
                    m = m0 + m0[0]

            # Add the reconstructed word to the dictionary
            dt = ajoute(dt, m)

            # Append the current word to the decoded result
            res += m

        i += 1

    return res


print("decodeLZW([33, 34, 95, 97, 35)=", decodeLZW([33, 34, 95, 97, 35]))
print("decodeLZW(encodeLZW('abracadabra')) =", decodeLZW(encodeLZW("abracadabra")))
print("decodeLZW(encodeLZW('Bonjour je suis un message, Bonjour je suis un second message')) =",
      decodeLZW(encodeLZW("Bonjour je suis un message, Bonjour je suis un second message")))

print()
print('-------------------')
print("Exercice 4.")
print()

file = open("testMurmure.txt", "r")
data = file.read()
file.close()

print("encodeLZW(data) =", encodeLZW(data))
decode = decodeLZW(encodeLZW(data))
print("decodeLZW(encodeLZW(data)) =", decode)
