import sys
import os
import unittest
from modules.open_digraph import *

root = os.path.normpath(os.path.join(__file__, './../..'))
sys.path.append(root)  # allows us to fetch files from the project root


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


class OpenDiagramTest(unittest.TestCase):
    def test_open_diagram(self):
        diagram = open_digraph()
        diagram.add_node('Aya')
        self.assertEqual(diagram.get_id_node_map().get(1).get_id(), 1)
        diagram.add_node(parents={1: 3})
        diagram.add_node('Pour', children={2: 4})
        diagram.add_node(children={2: 2})
        diagram.add_node(parents={4: 6})
        self.assertTrue(diagram.is_well_formed())
        diagram.add_input_node(2)
        diagram.add_output_node(3)
        diagram.add_output_node(4)
        diagram.add_input_node(4)
        self.assertTrue(diagram.is_well_formed())
        diagram.remove_parallel_edges(1, 2)
        diagram.remove_edge(1, 2)
        self.assertTrue(diagram.is_well_formed())
        diagram.remove_edge(6, 2)
        self.assertFalse(diagram.is_well_formed())
        diagram.add_edge(6, 2)
        self.assertTrue(diagram.is_well_formed())
        diagram.remove_node_by_id(5)
        self.assertTrue(diagram.is_well_formed())

if __name__ == '__main__':  # the following code is called only when
    unittest.main()  # precisely this file is run
