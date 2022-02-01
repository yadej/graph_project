from random import randint
import numpy as np


def random_symetrifc_int_matrix(n, bound, null_diag=True):
    a = np.symetric(n, n)
    a[0][1] = 1
    a[1][0] = a[0][1]

