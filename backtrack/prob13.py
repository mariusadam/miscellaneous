'''
Created on Dec 15, 2015

@author: Adam
'''
lista = [0, 23, 45, 67, 12,45, 32, 11, 12, 15]
n = len(lista)-1
lista = sorted(lista)
stiva = [0 for i in range(n + 1)]


def cifra_comuna(a, b):
    aux = b
    while a != 0:
        uc = a % 10
        while aux != 0:
            if aux % 10 == uc:
                return True
            aux = aux // 10
        a = a // 10
        aux = b
    return False

def solutie(k):
    nr = 0
    for i in range(1, k + 1):
        if stiva[i] == 1:
            nr += 1
    if nr <= 2:
        return False
    for i in range(1, k):
        if stiva[i] == 1:
            for j in range(i + 1, k + 1):
                if stiva[j] == 1:
                    if lista[i] == lista[j]:
                        return False
    for i in range(1, k):
        if stiva[i] == 1:
            poz = -1
            for j in range(i + 1, k + 1):
                if stiva[j] == 1:
                    poz = j
                    break
            if poz == -1:
                return True
            if not cifra_comuna(lista[i], lista[poz]):
                return False
    return True
    
def afisare(k):
    for i in range(1, k + 1):
        if stiva[i] == 1:
            print(lista[i], end=" ")
    print()

def gen_rec(k):
    for i in range(0, 2):
        stiva[k] = i
        if k == n:
            if solutie(k):
                afisare(k)
        else:
            gen_rec(k + 1)
            
def gen_it():
    k = 1
    stiva[k] = 0
    while k > 0:
        if stiva[k] < 2:
            stiva[k] += 1
            if k == n:
                if solutie(k):
                    afisare(k)
            else:
                k += 1
                stiva[k] = 0
        else:
            k -= 1

print("Recursiv:")     
gen_rec(1)    
print("Iterativ:")
gen_it()