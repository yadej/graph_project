import random
from modules.binaire import *
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
        """
        input: *args (tuple)
        output; g (bool_circ)
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
                    and '~' not in label and '|' not in label \
                    and label != '':
                g.add_input_id(g.new_id())
                g.add_node(label="entree" + str(p), children={m.get_id(): 1})
                p += 1

        return g

    @classmethod
    def from_binary_table(cls, table):

        """
        input: table (list)
        output; bc (boolean circuit)
        """

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
                        bc.add_node('~', {k - e: 1}, {p: 1})
                    else:
                        bc.add_edge((k - e, p))

        return bc

    def table_to_boolcirc_by_propo(self, table):
        s = gray_tp_propositionnell(table)
        return self.parse_parentheses(s)

    @classmethod
    def circrandom(cls, n, bound, input=-1, output=-1):
        # 1 - générer un graphe dirigé acyclique sans inputs ni outputs
        g = open_digraph.random(n, bound, form='DAG')
        AllNodes = list(g.get_nodes())
        # 2-1 - ajouter un input vers chaque noeud sans parent
        for u in list(g.get_nodes()):
            if not u.get_parent_ids():
                g.add_input_node(u.get_id())

        # 2-2 - ajouter un output depuis chaque noeud sans enfant
        for u in list(g.get_nodes()):
            if not u.get_children_ids() and u.get_parent_ids():
                g.add_output_node(u.get_id())

        AllNodesId = list(g.get_node_ids())

        if input > 0:
            while input < len(g.get_input_ids()):
                TabInput = list(g.get_input_ids())
                p = random.sample(TabInput, 2)
                for rem in p:
                    TabInput.remove(rem)
                g.set_input_ids(TabInput)
                k = g.new_id()
                g.add_node(label='', children={newParent: 1 for newParent in p})
                g.add_input_id(k)
            while input >= len(g.get_input_ids()):
                p = AllNodesId
                newInput = random.choice(p)
                g.add_input_id(newInput)

        if output > 0:
            while output > len(g.get_output_ids()):
                p = AllNodesId
                newInput = random.choice(p)
                g.add_output_node(label="", nodeId=newInput)

            while output < len(g.get_output_ids()):
                TabOutput = list(g.get_output_ids())
                p = random.sample(TabOutput, 2)
                for rem in p:
                    TabOutput.remove(rem)
                g.set_output_ids(TabOutput)
                k = g.new_id()
                g.add_node(label='', parents={newParent:1 for newParent in p})
                g.add_output_id(k)


        # 3
        for u in AllNodes:
            degP, degM = u.indegree(), u.outdegree()

            if degP == degM == 1:
                u.set_label('~')  # operateur unaire

            if degP == 1 and degM > 1:
                u.set_label('')  # copie

            if degP > 1 and degM == 1:
                u.set_label('op')  # operateur binaire (& ou |)

            if degP > 1 and degM > 1:
                uOp = g.new_id()
                g.add_node('op', parents=u.get_parent_ids())
                g.add_node('', parents={uOp: 1}, children=u.get_children_ids())
                g.remove_node_by_id(u.get_id())
        return g
