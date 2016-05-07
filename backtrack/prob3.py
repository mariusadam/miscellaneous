'''
Created on 28 dec. 2015

@author: marius
'''

def cont(stiva, k):
    ok = False
    for i in range(1,k):
        if stiva[i] == stiva[k]:
            return False
        elif abs(stiva[i] - stiva[k]) == 1:
            ok = True
    if k == 1: ok = True
    return ok

def bkt_it(n):
    '''
    n : numarul elementelor din vectorul permutat
    '''
    stiva = [i for i in range(n+1)]
    k = 1
    stiva[k] = 0
    while k > 0:
        if stiva[k] < n :
            stiva[k] += 1
            if cont(stiva, k):
                if k == n:
                    print(stiva[1:])
                else:
                    k += 1
                    stiva[k] = 0
        else:
            k -= 1

print("Iterativ:")        
bkt_it(3)
print("--------------------")
print("Recursiv:")
n = 3
stiva = [i for i in range(n + 1)]
def bkt_rec(k, stiva, n):
    '''
    k : nivelul curent din stiva
    stiva : stiva ce va fi folosita
    n : numarul de elemente
    '''
    for i in range(1, n + 1):
        stiva[k] = i
        if cont(stiva, k):
            if k == n:
                print(stiva[1:])
            else:
                bkt_rec(k + 1, stiva, n)
                
bkt_rec(1, stiva, n)