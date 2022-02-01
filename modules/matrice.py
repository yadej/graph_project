import random

def random_int_matrix(n, bound):
    return [[random.randrange(bound) for i in range(n)] for j in range(n)]
    

print(random_int_matrix(5,10))
