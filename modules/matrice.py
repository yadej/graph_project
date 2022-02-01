import numpy as np
import random

random_int_list = lambda n, bound: [random.randrange(bound) for i in range(n)]

def random_int_matrix(n, bound, null_diag=True, symetric=False, oriented=False, triangular=False):
    m = [random_int_list(n,bound) for _ in range(n)]
    
    if symetric:
        for i in range(n):
            for j in range(i):
                m[i][j] = m[j][i]
                
    if oriented:
        for i in range(n):
            for j in range(n):
                while m[i][j] == m[j][i] and i != j:
                    m[i][j] = random.randrange(n)
        
    if triangular:
        for i in range(n):
            for j in range(i):
                m[j][i] = 0
        
    if null_diag:
        for i in range(n):
            m[i][i] = 0
    
    return m

print(random_int_matrix(5, 10, oriented =True))
