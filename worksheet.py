import os
from modules import open_digraph
from modules.adjacency_matrix import random_int_matrix, graph_from_adjacency_matrix


def main():
    root_dir = os.path.dirname(os.path.abspath(__file__))

    graph = open_digraph.open_digraph()
    graph.add_node('Aya')
    graph.add_node(parents={1: 3})
    graph.add_node('Pour', children={2: 4})
    graph.add_node(children={2: 2})
    graph.add_node(parents={4: 6})
    graph.add_input_node(2)
    graph.add_output_node(3)
    graph.add_output_node(4)
    graph.add_input_node(4)
    print(f'{graph = }')
    print(f'{graph.is_well_formed() = }\n')

    graph.remove_parallel_edges((1, 2))
    print(f'{graph = }')
    print(f'{graph.is_well_formed() = }\n')

    graph.remove_edge((6, 2))
    print(f'{graph = }')
    print(f'{graph.is_well_formed() = }\n')

    graph.add_edge((6, 2))
    graph.remove_node_by_id(5)
    print(f'{graph = }')
    print(f'{graph.is_well_formed() = }\n')

    graph.remove_node_by_id(6)
    graph.add_edge((1, 3))
    print(f'{graph = }')
    print(f'{graph.is_well_formed() = }\n')

    def printMat(mat):
        for j in range(len(mat)):
            print(matrix[j])

    n = 7

    matrix = random_int_matrix(n, n, oriented=True)
    printMat(matrix)
    print()
    print(graph_from_adjacency_matrix(matrix))

    digraph = open_digraph.open_digraph.random(n, 1, 1, 2, form='loop-free')
    print(f'{digraph = }\n')

    b = digraph.adjacency_matrix()
    printMat(b)
    print(f'{digraph.dict_unique_id() = }\n')
    # p = random_int_matrix(10, 3, number_gen=(lambda: random.betavariate(1, 5)))

    gdot = root_dir + r'/digraph.dot'
    assert os.path.isfile(gdot)

    digraph.save_as_dot_file(gdot, verbose=False)
    print(f'{digraph = }')
    print(f'{digraph.is_cyclic() = }\n')

    c = digraph.adjacency_matrix()
    printMat(c)
    print()

    abc = digraph.from_dot_file(gdot)
    print(f'{abc = }')

    test = root_dir + '/test_bool.dot'

    testDis = digraph.from_dot_file(test, verbose=True)
    print(f'{testDis = }')
    # testDis.display(verbose=True)
    print(f'{testDis.is_cyclic() = }')
    # test_bool = open_digraph.bool_circ(testDis)

    print(f'{digraph.min_id() = }')
    print(f'{digraph.max_id() = }')

    x, y = digraph.connected_components()
    print(f'nb de composants connexes: {x}\n')
    print(f'{y = }\n')
    p = digraph.list()
    for i in p:
        print(i)
    print()

    print(f'{digraph.dijkstra(1) = }\n')

    d7 = digraph.from_dot_file('d7.dot')
    print(f'{d7.common_ancestor(5, 8) = }\n')
    print(f'{d7.tri_topologique() = }\n')


    print(d7.common_ancestor(5, 8))
    print(d7.tri_topologique())
    print(d7.noeuds_profondeur(5))
    print(d7.prof_OpD())
    print(d7.max_dist(1, 5))
    print(d7.max_dist(5, 1))

if __name__ == '__main__':
    main()
