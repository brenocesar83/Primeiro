import random

num = random.random()
#print(num)
num2 = random.randint(1, 60)
#print(num2)


def megasena(n):
    dezenas = []
    for i in range(n):
        dezenas.append(random.randint(1, 60))
    dezenas.sort()
    print("As {} dezenas escolhidas sao: ".format(n), end=" => ")
    print(dezenas)


#megasena(6)


def megasena2(n):
    dezenas = random.sample(range(1, 61), n)
    dezenas.sort()
    print("As {} dezenas escolhidas sao: ".format(n), end=" => ")
    print(dezenas)


megasena2(6)


# Acertar 15 dezenas de 01 a 25
# A estrategia adotada eh de divisao em blocos de 5
# 25/5 = 5 e nesse sentido, randomizar 3 dezenas em cada bloco
# privilegiado a maior sequencia que saiu que é 3-3-3-3-3
def lotofacil():
    dezenas = []
    for i in range(0, 3):
        dezenas.append(random.randint(1, 5))
        dezenas.append(random.randint(6, 10))
        dezenas.append(random.randint(11, 15))
        dezenas.append(random.randint(16, 20))
        dezenas.append(random.randint(21, 25))
        dezenas.sort()
    print(dezenas)

    
#lotofacil()


def lotofacil3(n, a, b, c, d, e):
    for i in range(n):
        dezenas = []
        dezenas.append(sorted(random.sample(range(1, 6), a)))
        dezenas.append(sorted(random.sample(range(6, 11), b)))
        dezenas.append(sorted(random.sample(range(11, 16), c)))
        dezenas.append(sorted(random.sample(range(16, 21), d)))
        dezenas.append(sorted(random.sample(range(21, 26), e)))
        print(dezenas)
    print()


lotofacil3(1, 4,4,3,3,3)
lotofacil3(1, 3,3,3,3,3)
lotofacil3(1, 3,2,4,3,3)
lotofacil3(1, 2,3,4,3,3)
lotofacil3(1, 3,2,3,3,4)


def lotofacil4():
  dezenas = []
  parcial1 = random.sample(range(1, 6), 3)
  parcial2 = random.sample(range(6, 11), 2)
  parcial3 = random.sample(range(11, 16), 4)
  parcial4 = random.sample(range(16, 21), 3)
  parcial5 = random.sample(range(21, 26), 3)
  for i in range(3):         
    dezenas.append(parcial1[i])
    dezenas.append(parcial2[i])
    dezenas.append(parcial3[i])
    dezenas.append(parcial4[i])
    dezenas.append(parcial5[i])
  dezenas.sort()
  print("As 15 dezenas para a LotoFacil sao: ", end=" => ")
  print(dezenas)

  
#lotofacil4()
