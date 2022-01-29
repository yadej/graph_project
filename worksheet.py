from modules.open_digraph import *
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
diagram.remove_edge(6, 2)
if diagram.is_well_formed():
    print('wo uho')
diagram.add_edge(6, 2)
diagram.remove_node_by_id(5)
if diagram.is_well_formed():
    print('wo uho')
print(diagram)
