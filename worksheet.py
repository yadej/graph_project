import random
from modules import open_digraph, matrice
import os

graph = open_digraph.open_digraph()
print(f'diagram = {graph}\n')

graph.add_node('Aya')
graph.add_node(parents={1: 3})
graph.add_node('Pour', children={2: 4})
graph.add_node(children={2: 2})
graph.add_node(parents={4: 6})
print(f'diagram = {graph}\n')

graph.add_input_node(2)
graph.add_output_node(3)
graph.add_output_node(4)
graph.add_input_node(4)
print(f'diagram = {graph}\n')

if graph.is_well_formed():
    print('wo uho')

graph.remove_parallel_edges((1, 2))
if graph.is_well_formed():
    print('wo uho')

graph.remove_edge((6, 2))
if graph.is_well_formed():
    print('wo uho')

graph.add_edge((6, 2))
graph.remove_node_by_id(5)
if graph.is_well_formed():
    print('wo uho')

graph.remove_node_by_id(6)
graph.add_edge((1, 3))
if graph.is_well_formed():
    print('wo uho')

print(graph)

n = 5
matrix = matrice.random_int_matrix(n, n, oriented=True)
for i in range(n):
    print(matrix[i])
print(matrice.graph_from_adjacency_matrix(matrix))

digraph = open_digraph.open_digraph.random(9, 10, form='loop-free')
print(digraph)

b = digraph.adjacency_matrix()
for i in range(9):
    print(b[i])
print(matrice.graph_from_adjacency_matrix(b))
print(digraph.dict_unique_id())
p = matrice.random_int_matrix(10, 3, number_gen=(lambda: random.betavariate(1, 5)))
for i in range(10):
    print(p[i])
existGDBPath = r"C:\Users\kids\PycharmProjects\projetinfo\diagraph.dot"
# existGDBPath = './diagraph.dot'
assert os.path.isfile(existGDBPath)
print(existGDBPath)

ellepath = os.path.dirname(existGDBPath)
print(ellepath)
print(os.access(ellepath, os.W_OK))

digraph.save_as_dot_file(existGDBPath, verbose=False)
