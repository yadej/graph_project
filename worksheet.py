from modules.open_digraph import *
from modules.matrice import *

# import inspect

d = open_digraph([1, 2, 3], [6], [node(0, 'a', [], [1])])
print(f'd = {d}\n')

print(f'methodes du module open_digraph = {dir(open_digraph)}')

diagram = open_digraph()
print(f'diagram = {diagram}\n')
diagram.add_node('Aya')
diagram.add_node(parents={1: 3})
diagram.add_node('Pour', children={2: 4})
diagram.add_node(children={2: 2})
diagram.add_node(parents={4: 6})
print(f'diagram = {diagram}\n')
diagram.add_input_node(2)
diagram.add_output_node(3)
diagram.add_output_node(4)
diagram.add_input_node(4)
print(f'diagram = {diagram}\n')
if diagram.is_well_formed():
    print('wo uho')
diagram.remove_parallel_edges((1, 2))
if diagram.is_well_formed():
    print('wo uho')
diagram.remove_edge((6, 2))
if diagram.is_well_formed():
    print('wo uho')
diagram.add_edge((6, 2))
diagram.remove_node_by_id(5)
if diagram.is_well_formed():
    print('wo uho')
diagram.remove_node_by_id(6)
diagram.add_edge((1, 3))
if diagram.is_well_formed():
    print('wo uho')
print(diagram)
n = 5
b = 5
k = random_int_matrix(n, b, oriented=True)
for i in range(n):
    print(k[i])

print(graph_from_adjacency_matrix(k))

w = open_digraph.random(9, 10, 2, 3)
print(w)
print(w.dict_unique_id())
