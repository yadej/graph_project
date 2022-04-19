import random
from modules.binaire import *
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
            # les noeuds ET/OU/OU-EXCLUSIF ie label='&'ou'|'ou'^' doivent avoir un output
            if n.get_label() == '&' or n.get_label() == '|' or n.get_label() == '^':
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
    def circrandom(cls, n, bound, inputs=0, outputs=0):
        """
        :param n: int
        :param bound: int
        :param input: int
        :param output: int
        :return: return g, an open digraph with a random configuration
        """
        # 1 - générer un graphe dirigé acyclique sans inputs ni outputs
        g = open_digraph.random(n, bound, form='DAG')
        AllNodes = list(g.get_nodes())
        AllNodeIds = list(g.get_node_ids())

        # 2-1 - ajouter un input vers chaque noeud sans parent
        for u in AllNodes:
            if not u.get_parent_ids():
                g.add_input_node(u.get_id())

        # 2-2 - ajouter un output depuis chaque noeud sans enfant
        for u in AllNodes:
            if not u.get_children_ids():
                g.add_output_node(u.get_id())

        print(f"{g.get_input_ids() = }")
        print(f"{g.get_output_ids() = }")
        # 2bis
        if inputs > 0:
            while inputs < len(g.get_input_ids()):  # trop d'inputs
                # on enleve deux input
                inputIds = list(g.get_input_ids())
                inputsToRemove = random.sample(inputIds, 2)

                for i in inputsToRemove:
                    inputIds.remove(i)

                g.set_input_ids(inputIds)

                # on rejoint ces 2 noeuds par un nouvel input
                k = g.new_id()
                g.add_node(label='', children={newParent: 1 for newParent in inputsToRemove})
                g.add_input_id(k)

            while inputs > len(g.get_input_ids()):  # si il y a pas assez
                # on ajoute un nouveau node en input
                k = g.new_id()
                g.add_node(label='', children={random.choice(AllNodeIds): 1})
                g.add_input_id(k)

        if outputs > 0:
            while outputs > len(g.get_output_ids()):  # si il y a pas assez d'output
                k = g.new_id()
                g.add_node(label='', parents={random.choice(AllNodeIds): 1})
                g.add_output_id(k)

            while outputs < len(g.get_output_ids()):  # trop
                outputIds = list(g.get_output_ids())
                outputsToRemove = random.sample(outputIds, 2)

                for i in outputsToRemove:
                    outputIds.remove(i)

                g.set_output_ids(outputIds)
                k = g.new_id()
                g.add_node(label='', parents={newParent: 1 for newParent in outputsToRemove})
                g.add_output_id(k)

        # 3
        for u in AllNodes:
            degP, degM = u.indegree(), u.outdegree()

            if degP == degM == 1:
                u.set_label('~')  # operateur unaire

            if degP == 1 and degM > 1:
                u.set_label('')  # copie

            if degP > 1 and degM == 1:
                if random.getrandbits(1):
                    u.set_label('&')
                else:
                    u.set_label('|')

            if degP > 1 and degM > 1:
                uOp = g.new_id()

                if random.getrandbits(1):
                    g.add_node('&', parents=u.get_parent_ids())
                else:
                    g.add_node('|', parents=u.get_parent_ids())

                g.add_node('', parents={uOp: 1}, children=u.get_children_ids())
                g.remove_node_by_id(u.get_id())

        print(f"{g.get_input_ids() = }")
        print(f"{g.get_output_ids() = }")
        return g

    @classmethod
    def adder(cls, a, b, carry):
        """
        :param a, b: registre de taille 2**n
        :param carry: bit de retenue
        :return: bit de retenue, registre de taille 2**n
        """
        n = len(a) >> 1  # log2(len(a))
        g = bool_circ()
        newCarry = 0
        rSum = 0

        if n == 0:
            ...

        return newCarry, rSum

    @classmethod
    def half_adder(cls, a, b):
        """
        :param a, b: registre de taille 2**n
        :return: bit de retenue, registre de taille 2**n qui contient la somme de a et b modulo 2**n
        """
        return cls.adder(a, b, 0)
