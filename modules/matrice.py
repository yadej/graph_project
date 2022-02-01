import numpy as np
import random
    

random_int_list = lambda n, bound: [random.randrange(bound) for i in range(n)]

def random_int_matrix(n, bound, null_diag=True):
    return [random_int_list(n,bound) for _ in range(n)]


def random_symetrifc_int_matrix(n, bound, null_diag=True):
    a = np.symetric(n, n)
    a[0][1] = 1
    a[1][0] = a[0][1]