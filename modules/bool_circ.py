from modules.node import node
from modules.open_digraph import open_digraph


class bool_circ(open_digraph):

    def __init__(self, g=None):
        if isinstance(g, open_digraph):
            super().__init__(g.get_input_ids(), g.get_output_ids(), g.get_nodes())
        if not g.is_well_formed():
            raise Exception('is not a boolean circuit')

    def is_well_formed(self):
        """
        inputs : none
        outputs : boolean (bool)
        returns if boolean_circuit is really a boolean circuit
        """
        # doit etre acyclique
        if self.is_cyclic():
            return False

        for n in self.get_nodes():
            # les noeuds copie ie label='' doivent avoir un input
            if n.get_label() == '' and len(n.get_children_ids()) != 1:
                return False
            # les noeuds ET/OU ie label='&'ou'|' doivent avoir un output
            if n.get_label() == '&' or n.get_label() == '|':
                if len(n.get_parent_ids()) != 1:
                    return False
            # les noeuds NON ie label='~' doivent avoir un input et un output
            if n.get_label() == '~':
                if len(n.get_parent_ids()) != 1 or len(n.get_children_ids()) != 1:
                    return False
        return True

    @classmethod
    def parse_parentheses(cls, s):
        g = bool_circ(open_digraph(outputs=[1], nodes={0: node(0, '', {}, {1: 1}), 1: node(1, '', {0: 1}, {})}))
        current_node = 0
        s2 = ''

        for c in s:
            if c == '(':
                g.get_node_by_id(current_node).set_label(s2)
                # creer un parent a current node et faire en sorte que ce parent soit desormais current node
                g.get_node_by_id(current_node).set_parent_ids({2: 1})
                current_node = 2
                s2 = ''
            elif c == ')':
                g.get_node_by_id(current_node).set_label(s2)
                # changer current_node pour qu'il prenne l'id de son fils
                s2 = ''
            else:
                s2 += c

        return g
