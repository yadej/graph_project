import unittest
from modules.open_digraph import *


class InitTest(unittest.TestCase):
    def test_init_node(self):
        n0 = node(0, 'i', {}, {1: 1})
        self.assertEqual(n0.id, 0)
        self.assertEqual(n0.label, 'i')
        self.assertEqual(n0.parents, {})
        self.assertEqual(n0.children, {1: 1})
        self.assertIsInstance(n0, node)
        self.assertIsNot(n0.copy(), n0)


class NodeTest(unittest.TestCase):
    def setUp(self):
        self.n0 = node(0, 'a', [], [1])

    def test_get_id(self):
        self.assertEqual(self.n0.get_id(), 0)

    def test_get_label(self):
        self.assertEqual(self.n0.get_label(), 'a')


class OpenDigraphTest(unittest.TestCase):
    def test_open_digraph(self):
        digraph = open_digraph()
        digraph.add_node('Aya')
        self.assertEqual(digraph.get_id_node_map().get(0).get_id(), 0)
        digraph.add_node(parents={0: 3})
        digraph.add_node('Pour', children={1: 4})
        digraph.add_node(children={2: 2})
        digraph.add_node(parents={3: 6})
        self.assertTrue(digraph.is_well_formed())
        digraph.add_input_node(2)
        digraph.add_output_node(3)
        digraph.add_output_node(4)
        digraph.add_input_node(4)
        self.assertTrue(digraph.is_well_formed())
        digraph.remove_parallel_edges((1, 2))
        self.assertTrue(digraph.is_well_formed())
        digraph.remove_edge((5, 2))
        self.assertFalse(digraph.is_well_formed())
        digraph.add_edge((5, 2))
        self.assertTrue(digraph.is_well_formed())
        digraph.remove_node_by_id(5)
        self.assertTrue(digraph.is_well_formed())
        digraph.remove_node_by_id(6)
        digraph.add_edge((1, 3))
        self.assertTrue(digraph.is_well_formed())
        digraph2 = open_digraph(nodes=digraph.get_nodes())
        digraph2.shift_indices(3)
        self.assertTrue(digraph2.is_well_formed())
        digraph2.iparallel(open_digraph.random(5, 10))
        self.assertTrue(digraph2.is_well_formed())
        digraph3 = digraph2.parallel(open_digraph.random(5, 10))
        self.assertTrue(digraph3.is_well_formed())
        self.assertTrue(digraph2.dijkstra(1)[1].get(0) in digraph2.dijkstra(1)[0])
        d7 = open_digraph.from_dot_file('d7.dot')
        self.assertEqual(d7.common_ancestors(5, 8), {0: (2, 3), 1: (1, 1), 3: (1, 2)})
        self.assertEqual(d7.tri_topologique(), [[0, 1, 2], [3, 4], [5, 6], [7, 8, 9]])


if __name__ == '__main__':
    unittest.main()
