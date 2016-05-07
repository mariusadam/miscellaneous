'''
Created on 7 ian. 2016

@author: marius
'''
suma_curenta = 0
s = 261      # suma de platit
nr_sol = 0  # numarul de solutii
m = [1, 5, 10]                            # m[i] = valoarea monedei i 
n = len(m)
nr = [s // m[i] for i in range(len(m))]     # nr[i] = numarul de monede de tipul i

def consistent(x, m, nr, n):
    global s, suma_curenta
    if len(x) > n:
        return False
    suma_curenta = 0
    for i in range(len(x)):
        suma_curenta += m[i] * x[i]
    return suma_curenta <= s          #suma pana la un anumit pas trebuie sa fie <= s

def solutie(x, m, nr, n):
    global s, suma_curenta
    return suma_curenta == s and len(x) == n

def tipareste(x, m, nr, n):
    global nr_sol
    nr_sol += 1
    print("---------------------")
    for i in range(n):
        print(x[i], "monede cu valoarea", m[i])
    print("---------------------")   

def back_rec(x, m, nr, n):
    if len(x) >= n:
        return
    x.append(0)
    for i in range(nr[len(x) - 1] + 1):
        x[-1] = i
        if consistent(x, m, nr, n):
            if solutie(x, m, nr, n):
                tipareste(x, m, nr, n)
            back_rec(x, m, nr, n)
    x.pop()       
    
def back_it(x, m, nr, n):
    x.append(-1)
    while len(x) > 0:
        if x[-1] < nr[len(x) - 1]:
            x[-1] += 1
            if consistent(x, m, nr, n):
                if solutie(x, m , nr, n):
                    tipareste(x, m, nr, n)
                elif len(x) < n:
                    x.append(-1)
        else:
            x.pop()

print("Iterativ:")
back_it([], m, nr, n)
nr_sol_it = nr_sol
if nr_sol == 0:
    print("Nu exista solutie!")
else:
    print("Recursiv:")
    nr_sol = 0
    back_rec([], m, nr, n)
print(nr_sol_it, nr_sol)

    