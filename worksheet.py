import os

from modules.bool_circ import bool_circ
from modules.open_digraph import open_digraph
from modules.adjacency_matrix import random_int_matrix, graph_from_adjacency_matrix
from modules.binaire import *

dotFolder = os.path.dirname(os.path.abspath(__file__)) + r'/dot_files/'


def printMat(mat):
    for j in range(len(mat)):
        print(mat[j])
    print()


def main():
    """
    graph = open_digraph()
    graph.add_node('Aya')
    graph.add_node(parents={0: 3})
    graph.add_node('Pour', children={1: 4})
    graph.add_node(children={2: 2})
    graph.add_node(parents={3: 6})
    graph.add_input_node(2)
    graph.add_output_node(3)
    graph.add_output_node(4)
    graph.add_input_node(4)
    print(f'{graph = }')
    print(f'{graph.is_well_formed() = }\n')

    graph.remove_parallel_edges((1, 2))
    print(f'{graph = }')
    print(f'{graph.is_well_formed() = }\n')

    graph.remove_edge((5, 2))
    print(f'{graph = }')
    print(f'{graph.is_well_formed() = }\n')

    graph.add_edge((5, 2))
    graph.remove_node_by_id(5)
    print(f'{graph = }')
    print(f'{graph.is_well_formed() = }\n')

    graph.remove_node_by_id(6)
    graph.add_edge((1, 3))
    print(f'{graph = }')
    print(f'{graph.is_well_formed() = }\n')

    graph.shift_indices(3)
    print(f'{graph = }')
    print(f'{graph.is_well_formed() = }\n')

    n = 7

    matrix = random_int_matrix(n, n, oriented=True)

    print('matrix = ')
    printMat(matrix)

    print(graph_from_adjacency_matrix(matrix))

    digraph = open_digraph.random(n, 1, 1, 2, form='loop-free')
    print(f'{digraph = }\n')

    b = digraph.adjacency_matrix()

    print('b = ')
    printMat(b)

    print(f'{digraph.dict_unique_id() = }\n')
    # p = random_int_matrix(10, 3, number_gen=(lambda: random.betavariate(1, 5)))

    gdot = dotFolder + r'digraph.dot'
    assert os.path.isfile(gdot)

    digraph.save_as_dot_file(gdot, verbose=False)
    print(f'{digraph = }')
    print(f'{digraph.is_cyclic() = }\n')

    c = digraph.adjacency_matrix()
    print('c = ')
    printMat(c)

    abc = digraph.from_dot_file(gdot)
    print(f'{abc = }')

    test = dotFolder + 'test_bool.dot'

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

    d7 = open_digraph.from_dot_file(dotFolder + r'd7.dot')
    print(f'{d7.dijkstra(1) = }\n')
    print(f'{d7.shortest_path(1, 9) = }\n')
    print(f'{d7.common_ancestors(5, 8) = }\n')
    print(f'{d7.tri_topologique() = }\n')
    print(f'{d7.node_depth(6) = }\n')
    print(f'{d7.depth() = }\n')
    print(f'{d7.max_dist(1, 5) = }\n')
    print(f'{d7.max_dist(5, 1) = }\n')
    print(f'{d7.max_dist(9, 1) = }\n')

    tmp = d7.copy()
    tmp.fusion(1, 4)
    tmp.get_node_by_id(1).set_label('1, 4')
    tmp.save_as_dot_file(dotFolder + r'tmp.dot')

    tmp2 = bool_circ.parse_parentheses('((x0)&((x1)&(x2)))|((x1)&(~(x2)))')
    tmp2.save_as_dot_file(dotFolder + r'tmp2.dot')

    tmp3 = bool_circ.parse_parentheses("((x0)&((x1)&(x2)))|((x1)&(~(x2)))", "((x0)&(~(x1)))|(x2)")
    tmp3.save_as_dot_file(dotFolder + r'tmp3.dot')

    tmp4 = bool_circ.parse_parentheses("((x0)&(x1)&(x2))|((x1)&(~(x2)))")
    tmp4.save_as_dot_file(dotFolder + r'tmp4.dot')

    tmp5 = bool_circ.from_binary_table('1110001000111111')
    tmp5.save_as_dot_file(dotFolder + r'tmp5.dot')
    """
    print(f'{gray_code(2) = }\n')

    pr = K_map('1110001000111111')

    print('K_map(\'1110001000111111\') = ')
    printMat(pr)

    print(f'{[pr[0:2][0][0:2], pr[0:2][1][0:2]] = }\n')

    print(f"{gray_tp_propositionnell('1110001000111111') = }\n")

    rg = bool_circ.circrandom(8, 2, inputs=3, outputs=2)
    rg.save_as_dot_file(dotFolder + r'random_bool_circ.dot')

    adderTest = bool_circ.adder("11", "101", 1)[1]
    print(adderTest)
    adderTest.save_as_dot_file(dotFolder + r'testAdder.dot')

    binaryTest = bool_circ.int_to_boolcirc(11)
    print(binaryTest)
    binaryTest.save_as_dot_file(dotFolder + r'testBinary.dot')
    # Test des portes + copies
    TestPorteEt = bool_circ(open_digraph())
    TestPorteOu = bool_circ(open_digraph())
    TestPorteOuExclusif = bool_circ(open_digraph())
    TestPorteNon = bool_circ(open_digraph())
    parentN = 0
    for label in ["0", "1"]:
        TestPorteEt.add_node(label=label)
        TestPorteEt.add_node(label="&", parents={parentN: 1})
        TestPorteEt.add_node(label="", parents={parentN + 1: 1})
        TestPorteEt.add_node(label=label)
        TestPorteEt.add_node(label="&", parents={parentN + 3: 1})
        TestPorteEt.add_node(label="", parents={parentN + 4: 1})
        TestPorteOu.add_node(label=label)
        TestPorteOu.add_node(label="|", parents={parentN: 1})
        TestPorteOu.add_node(label="", parents={parentN + 1: 1})
        TestPorteOu.add_node(label=label)
        TestPorteOu.add_node(label="|", parents={parentN + 3: 1})
        TestPorteOu.add_node(label="", parents={parentN + 4: 1})
        TestPorteOuExclusif.add_node(label=label)
        TestPorteOuExclusif.add_node(label="^", parents={parentN: 1})
        TestPorteOuExclusif.add_node(label="", parents={parentN + 1: 1})
        TestPorteOuExclusif.add_node(label=label)
        TestPorteOuExclusif.add_node(label="^", parents={parentN + 3: 1})
        TestPorteOuExclusif.add_node(label="", parents={parentN + 4: 1})
        TestPorteNon.add_node(label=label)
        TestPorteNon.add_node(label="~", parents={parentN: 1})
        TestPorteNon.add_node(label="", parents={parentN + 1: 1})
        TestPorteNon.add_node(label=label)
        TestPorteNon.add_node(label="~", parents={parentN + 3: 1})
        TestPorteNon.add_node(label="", parents={parentN + 4: 1})
        parentN += 6

    TestPorteEt.porte_Et(0, 6)
    TestPorteOu.porte_Ou(0, 6)
    TestPorteOuExclusif.porte_Ou_Exculsif(0, 6)
    TestPorteNon.porte_Non(0, 6)
    adderTest.evaluate()
    print(TestPorteEt)
    TestPorteEt.save_as_dot_file(dotFolder + r'testPorteEt.dot')
    TestPorteOu.save_as_dot_file(dotFolder + r'testPorteOu.dot')
    TestPorteOuExclusif.save_as_dot_file(dotFolder + r'TestPorteOuExclusif.dot')
    TestPorteNon.save_as_dot_file(dotFolder + r'testPorteNon.dot')
    adderTest.save_as_dot_file(dotFolder + r'testEvaluate.dot')

    encodeur = bool_circ.encodeur()
    print(encodeur)
    encodeur.save_as_dot_file(dotFolder + r'testEncodeur.dot')

    decodeur = bool_circ.decodeur()
    print(decodeur)
    decodeur.save_as_dot_file(dotFolder + r'testDecodeur.dot')
    # Test Association XOR
    TestAssocXor = bool_circ(open_digraph())
    TestAssocXor.add_node(label="^")
    TestAssocXor.add_node(label="^", children={0: 1})
    TestAssocXor.add_node(label="1", children={0: 1})
    TestAssocXor.add_node(label="0", children={0: 1})
    TestAssocXor.add_node(label="1", children={1: 1})
    TestAssocXor.add_node(label="0", children={1: 1})
    TestAssocXor.add_output_node(0)
    TestAssocXor.assosXOR(1)
    TestAssocXor.save_as_dot_file(dotFolder + r'testAssocXor.dot')

    # Assoc Copies
    TestAssocCopie = bool_circ(open_digraph())
    TestAssocCopie.add_node(label="")
    TestAssocCopie.add_node(label="", parents={0: 1})
    TestAssocCopie.add_node(label="1", parents={0: 1})
    TestAssocCopie.add_node(label="0", parents={0: 1})
    TestAssocCopie.add_node(label="1", parents={1: 1})
    TestAssocCopie.add_node(label="0", parents={1: 1})
    TestAssocCopie.add_input_node(0)
    TestAssocCopie.assosCopies(0)
    TestAssocCopie.save_as_dot_file(dotFolder + r'testAssocCopies.dot')

    # Test involution Xor
    # Cela marche pour pair ou impaire
    TestInvolutionXor = bool_circ(open_digraph())
    TestInvolutionXor.add_node()
    TestInvolutionXor.add_node(label="^", parents={0: 3})
    TestInvolutionXor.add_node(label="1", children={0: 1})
    TestInvolutionXor.add_node(label="1", children={1: 1})
    TestInvolutionXor.add_node(label="0", children={1: 1})
    TestInvolutionXor.add_node(parents={0: 1})
    TestInvolutionXor.add_node(parents={0: 1})
    TestInvolutionXor.add_node(parents={1: 1})
    TestInvolutionXor.involutionXOR(0)
    TestInvolutionXor.save_as_dot_file(dotFolder + r'testInvolutionXOR.dot')

    # Test effacement
    TestEffacement = bool_circ(open_digraph())
    TestEffacement.add_node("&")
    TestEffacement.add_node(label="1", children={0: 1})
    TestEffacement.add_node(label="0", children={0: 1})
    TestEffacement.add_node(label="", parents={0: 1})
    TestEffacement.effacement(0)
    TestEffacement.save_as_dot_file(dotFolder + r'testEffacement.dot')

    #Test Non travers Xor
    TestNonTraverXor = bool_circ(open_digraph())
    TestNonTraverXor.add_node(label="^")
    TestNonTraverXor.add_node(label="~", children={0: 1})
    TestNonTraverXor.add_node(label="1", children={1: 1})
    TestNonTraverXor.add_node(label="1", children={0: 1})
    TestNonTraverXor.add_node(label="0", children={0: 1})
    TestNonTraverXor.add_node(label="", parents={0: 1})
    TestNonTraverXor.nonTraverXOR(1)
    TestNonTraverXor.save_as_dot_file(dotFolder + r'testNonTraverXor.dot')

    #Test Non travers Copies
    TestNonTraverCopies = bool_circ(open_digraph())
    TestNonTraverCopies.add_node(label="~")
    TestNonTraverCopies.add_node(label="", parents={0: 1})
    TestNonTraverCopies.add_node(parents={1: 1})
    TestNonTraverCopies.add_node(parents={1: 1})
    TestNonTraverCopies.add_node(label="1", children={0: 1})
    TestNonTraverCopies.nonTraversCopies(0)
    TestNonTraverCopies.save_as_dot_file(dotFolder + r'testNonTraverCopies.dot')

    # Test Involution Non
    TestInvolutionNon = bool_circ(open_digraph())
    TestInvolutionNon.add_node(label="~")
    TestInvolutionNon.add_node(label="~", parents={0: 1})
    TestInvolutionNon.add_node(label="1", parents={1: 1})
    TestInvolutionNon.add_node(label="", children={0: 1})
    TestInvolutionNon.involutionNon(0)
    TestInvolutionNon.save_as_dot_file(dotFolder + r'testInvolutionNon.dot')


if __name__ == '__main__':
    main()
