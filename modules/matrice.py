import random
from open_digraph import *

random_int_list = lambda n, bound: [random.randrange(bound) for i in range(n)]

def random_int_matrix(n, bound, null_diag=True):
    return [random_int_list(n,bound) for _ in range(n)]
    
def random_oriented_int_matrix(n, bound,null_diag=True):
    m =  random_int_matrix(n,bound)
    for i in range(n):
        for j in range(n):
            if j == i and null_diag:
                m[i][i] = 0
            elif i == j:
                continue
            else:
                while m[i][j] == m[j][i]:
                    m[i][j] = random.randrange(bound)
            return m
            
print(random_oriented_int_matrix(5,10))

