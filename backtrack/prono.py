'''
Created on 5 ian. 2016

@author: marius
'''
v = ['x', '1', '2']

def consistent(x, dim):
    nr = 0
    for i in range(len(x)):
        if v[x[i]] == '1':
            nr += 1
    if nr > 2:
        return False
    return True

def solutie(x, dim):
    if len(x) != dim or v[x[-1]] == 'x':
        return False
    return True

def tipareste(x, dim):
    for i in range(dim):
        print(v[x[i]], end=" ")
    print()
        
def back_rec(x, dim):
    if len(x) >= dim:
        return
    x.append(0)
    for el in range(3):
        x[-1] = el
        if consistent(x, dim):
            if solutie(x, dim):
                tipareste(x, dim)
            back_rec(x, dim)
    x.pop()
  
def back_it(x, n):
    x.append(-1)
    print(len(x), n)
    while len(x) > 0 :
        if x[-1] < 2:
            x[-1] += 1
            if consistent(x, n) and len(x) <= n:
                if solutie(x, n):
                    tipareste(x, n)
                else:
                    x.append(-1)
        else:
            x.pop()
            

n = 5
print("Recursiv:")  
back_rec([], n)
print("Iterativ:")
back_it([], n)