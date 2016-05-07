'''
Created on 5 ian. 2016

@author: marius
'''
nr = 0
def consistent(x, dim):
    if len(set(x)) != len(x):
        return False
    last_x = len(x) - 1
    last_y = x[-1]
    for i in range(len(x) - 1):
        if abs(i - last_x) == abs(x[i] - last_y):
            return False
    return True

def solutie(x, dim):
    return len(x) == dim

def tipareste(x, dim):
    global nr
    nr += 1
    tabla = []
    for i in range(dim):
        tabla.append(['0'] * dim)
    for i in range(dim):
        tabla[i][x[i]] = "x"  
    for line in tabla:
        print(" ".join(line))
    print("-" * dim * 2)
        
def back(x, dim):
    if len(x) >= dim:
        return
    x.append(0)
    for el in range(dim):
        x[-1] = el
        if consistent(x, dim):
            if solutie(x, dim):
                tipareste(x, dim)
            back(x, dim)
    x.pop()
    
back([], 10)
print(nr)