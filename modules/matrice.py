import random
import modules.open_digraph


def random_int_list(n, bound):
    return [random.randrange(bound) for _ in range(n)]


def random_int_matrix(n, bound, null_diag=True, symetric=False, oriented=False, triangular=False,
                      number_generator=None):
    if number_generator is None:
        m = [random_int_list(n, bound) for _ in range(n)]
    else:
        m = [[int(bound * number_generator()) for _ in range(n)] for _ in range(n)]
    
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


def graph_from_adjacency_matrix(m):
    a = modules.open_digraph.open_digraph.empty()
    for _ in range(len(m)):
        a.add_node()
    for i in range(len(m)):
        for j in range(len(m)):
            for _ in range(m[i][j]):
                a.add_edge((i, j))
    return a
