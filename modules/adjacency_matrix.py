from random import randrange
from modules import open_digraph


def random_int_list(n, bound):
    """

    inputs : n: int, bound: int
    outputs : list of random int between 0 and bound (int list)
    """
    return [randrange(bound) for _ in range(n)]


def random_int_matrix(n, bound, null_diag=True, symetric=False, oriented=False, triangular=False, number_gen=None):
    """

    inputs : n: int, bound: int, null_diag: bool, symetric: bool, oriented: bool, triangular: bool, number_gen: int
    outputs : generate n*n matrix with random numbers between 0 and bound (matrix)
    """
    if number_gen is None:
        matrix = [random_int_list(n, bound) for _ in range(n)]
    else:
        matrix = [[int(bound * number_gen()) for _ in range(n)] for _ in range(n)]

    if symetric:
        for i in range(n):
            for j in range(i):
                matrix[i][j] = matrix[j][i]

    if oriented:
        for i in range(n):
            for j in range(n):
                while matrix[i][j] == matrix[j][i] and i != j:
                    matrix[i][j] = randrange(n)

    if triangular:
        for i in range(n):
            for j in range(i):
                matrix[j][i] = 0

    if null_diag:
        for i in range(n):
            matrix[i][i] = 0

    return matrix


def graph_from_adjacency_matrix(m):
    """
    input : m (matrix)
    output : graph from adjacency matrix (graph)
    """
    graph = open_digraph.open_digraph()

    for _ in range(len(m)):
        graph.add_node()

    for i in range(len(m)):
        for j in range(len(m)):
            for _ in range(m[i][j]):
                graph.add_edge((i, j))

    return graph
