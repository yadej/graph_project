import random

random_int_list = lambda n, bound: [random.randrange(bound) for i in range(n)]

def random_int_matrix(n, bound, null_diag=True):
    
