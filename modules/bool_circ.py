from modules.node import node
from modules.open_digraph import open_digraph


class bool_circ(open_digraph):

    def __init__(self, g=None):
        if g is None:
            super.__init__()
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
    def parse_parentheses(cls, *args):
        """g = bool_circ(open_digraph(outputs=[1], nodes=[node(0, '', {}, {1: 1}), node(1, '', {0: 1}, {})]))
        current_node = 0
        for s in args:
            s = "(" + s + ")"
            s2 = ''
            for c in s:
                if c == '(':
                    g.get_node_by_id(current_node).set_label(g.get_node_by_id(current_node).get_label() + s2)

                    newId = g.new_id()
                    g.add_node(children={current_node: 1})
                    current_node = newId
                    s2 = ''
                elif c == ')':
                    g.get_node_by_id(current_node).set_label(g.get_node_by_id(current_node).get_label() + s2)
                    current_node = list(g.get_node_by_id(current_node).get_children_ids().keys())[0]
                    s2 = ''
                else:
                    s2 += c
        """

        g = bool_circ(open_digraph())
        num = 0
        current_node = 0
        for s in args:
            # On va paralleliser g et par
            newlabel = "sortie " + str(num)
            num += 1
            par = bool_circ(open_digraph(nodes=[node(0, newlabel, {}, {})]))
            s = "(" + s + ")"
            s2 = ''
            for c in s:
                if c == '(':
                    par.get_node_by_id(current_node).set_label(par.get_node_by_id(current_node).get_label() + s2)
                    newId = par.new_id()
                    par.add_node(children={current_node: 1})
                    current_node = newId
                    s2 = ''
                elif c == ')':
                    par.get_node_by_id(current_node).set_label(par.get_node_by_id(current_node).get_label() + s2)
                    current_node = list(par.get_node_by_id(current_node).get_children_ids().keys())[0]
                    s2 = ''
                else:
                    s2 += c
            g.iparallel(par)

        k = 0
        while k != len(g.get_nodes()):
            lab = g.get_node_by_id(k).get_label()
            if lab == "":
                k += 1
                continue
            if lab.__contains__("&") or lab.__contains__("~") \
                    or lab.__contains__("|"):
                g.get_node_by_id(k).set_label(lab[0])
                for i in list(g.get_node_by_id(k).get_children_ids()):
                    if lab[0] in g.get_node_by_id(i).get_label():
                        g.fusion(k, i)
                k += 1
                continue
            new = -1
            for i in range(k + 1, len(g.get_nodes())):
                if g.get_node_by_id(i).get_label() == lab and g.get_node_by_id(i).get_label() != "":
                    new = i
                    break
            if new != -1:
                g.fusion(k, new)
            else:
                k += 1
        p = 0
        for m in list(g.get_nodes()):

            label = m.get_label()
            if "sortie" not in label and "&" not in label \
                    and '~' not in label and '|' not in label\
                    and label != '':
                g.add_input_id(g.new_id())
                g.add_node(label="entree" + str(p), children={m.get_id(): 1})
                p += 1

        return g


    @classmethod
    def from_binary_table(cls, table):
        # We have at least 3 on depth and max 4 on depth
        bc = bool_circ(open_digraph(nodes=[node(0, '', {}, {})]))
        w = len(table) - 1 if len(table) > 5 else len(table)
        k = 0
        while w > 0:
            w = w // 2
            bc.add_node()
            k += 1
        for x, char in enumerate(table):
            if char == "1":
                p = bc.new_id()
                bc.add_node(label="&", children={0: 1})
                m = '0' * (k - len(bin(x)[2:])) + bin(x)[2:]
                for e, i in enumerate(m):

                    if i == '0':
                        bc.add_node('~', {k-e: 1}, {p: 1})
                    else:
                        bc.add_edge((k-e, p))

        return bc

    def gray_code(self, n):
        g = ['0', '1']
        if n <= 0:
            return []
        for i in range(n-1):
            g1 = ['1' + i for i in g][::-1]
            g0 = ['0' + i for i in g]
            g = g0 + g1
        return g

    def K_map(self, s1):
        w = len(s1) - 1 if len(s1) > 5 else len(s1)
        k = 0
        while w > 0:
            w = w // 2
            k += 1
        if k % 2 == 1:
            t1 = self.gray_code(k // 2 + 1)
            t2 = self.gray_code(k // 2)
        else:
            t1 = self.gray_code(k // 2)
            t2 = self.gray_code(k // 2)
        k1 = len(t1)
        k2 = len(t2)
        t = [[0 for _ in range(k2)] for _ in range(k1)]

        for i in range(k1):
            for j in range(k2):
                p = int(t1[i] + t2[j], 2)
                if s1[p] == '1':
                    t[i][j] = 1
                else:
                    t[i][j] = 0
        return t
