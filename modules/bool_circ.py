import random
from modules.binaire import gray_tp_propositionnell
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
            # les noeuds copie ie label='0' ou '1' doivent avoir un input
            if n.get_label() == '' or n.get_label() == '1' or n.get_label() == '0' and len(n.get_children_ids()) != 1:
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
        :param inputs: int
        :param outputs: int
        :return: return g, an open digraph with a random configuration
        """
        # 1 - générer un graphe dirigé acyclique sans inputs ni outputs
        g = open_digraph.random(n, bound, form='DAG')
        AllNodes = list(g.get_nodes())
        AllNodeIds = list(g.get_node_ids())

        # 2-1 - ajouter un input vers chaque noeud sans parent
        for u in AllNodes:
            if not u.get_parent_ids() and u.get_children_ids():
                g.add_input_node(u.get_id())

        # 2-2 - ajouter un output depuis chaque noeud sans enfant
        for u in AllNodes:
            if not u.get_children_ids() and u.get_parent_ids():
                g.add_output_node(u.get_id())

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
                g.add_input_node(k)
                AllNodes.append(g.get_node_by_id(k))

            while inputs > len(g.get_input_ids()):  # si il y a pas assez
                # on ajoute un nouveau node en input
                k = g.new_id()
                g.add_node(label='', children={random.choice(AllNodeIds): 1})
                g.add_input_node(k)

        if outputs > 0:
            while outputs > len(g.get_output_ids()):  # si il y a pas assez d'output
                k = g.new_id()
                g.add_node(label='', parents={random.choice(AllNodeIds): 1})
                g.add_output_node(k)

            while outputs < len(g.get_output_ids()):  # trop
                outputIds = list(g.get_output_ids())
                outputsToRemove = random.sample(outputIds, 2)
                for i in outputsToRemove:
                    outputIds.remove(i)

                g.set_output_ids(outputIds)
                k = g.new_id()
                g.add_node(label='', parents={newParent: 1 for newParent in outputsToRemove})
                g.add_output_node(k)
                AllNodes.append(g.get_node_by_id(k))

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
                uParent = u.get_parent_ids()
                uChildren = u.get_children_ids()
                if random.getrandbits(1):
                    g.add_node('&', parents={x: y for x, y in uParent.items()})
                else:
                    g.add_node('|', parents={x: y for x, y in uParent.items()})

                g.add_node('', parents={uOp: 1}, children={x: y for x, y in uChildren.items()})
                g.remove_node_by_id(u.get_id())
        return g

    @classmethod
    def adder(cls, a, b, carry):
        """
        :param a, b: registre de taille 2**n
        :param carry: bit de retenue
        :return: bit de retenue, registre de taille 2**n
        """
        n = 0
        tailleRegistre = len(a)
        if tailleRegistre < len(b):
            tailleRegistre = len(b)
        while tailleRegistre > 1:
            tailleRegistre //= 2
            n += 1
        a = "0" * (2**n - len(a)) + a
        b = "0" * (2**n - len(b)) + b
        # Calcul Somme binaire de a et b modulo 2**n

        # rajout des 0 manquant pour que cela rentre dans 2**n
        sommeBinaire = ''.join(["1" if i == j == "1" else "0" for i, j in zip(a, b)])
        print(sommeBinaire)
        r = bool_circ(open_digraph(nodes=[node(0, '|', {}, {})]))
        newCarry = 0 if int(a,2) + int(b, 2) < 2** (2**n) or carry == 0 else 1

        # Node 0
        # r.add_node(label="|")
        # Node 1
        r.add_node(label="&", children={0: 1})
        # Node 2
        r.add_node(label="&", children={0: 1})
        # Node 3
        r.add_node(label="^")
        # Node 4
        r.add_node(label="", children={3: 1, 1: 1})
        # Node 5
        r.add_node(label="", children={3: 1, 1: 1})
        # Node 6
        r.add_node(label="^", children={5: 1})
        # Node 7
        r.add_node(label="", children={6: 1, 2: 1})
        # Node 8
        r.add_node(label="", children={6: 1, 2: 1})
        # C 9
        r.add_input_node(4)
        # A 10
        r.add_input_node(7)
        # B 11
        r.add_input_node(8)
        # carry 12
        r.add_output_node(0)
        # r 13
        r.add_output_node(3)
        while n > 0:
            n -= 1
            # carry
            newAdder = r.copy()
            r.shift_indices(r.max_id() - r.min_id())
            attacheOutput = min(newAdder.get_output_ids())
            # C
            attacheInput = min(r.get_input_ids()) + 1
            r.iparallel(newAdder)
            # attacheInput = max(r.get_input_ids())
            print(f"{attacheOutput =}")
            print(f"{r.get_output_ids() =}")
            print(f"{attacheInput =}")
            print(f"{r.get_input_ids() =}")
            r.get_input_ids().remove(attacheInput)
            r.get_output_ids().remove(attacheOutput)
            r.add_edge((attacheOutput, attacheInput))
        j = 0
        turn = True
        for i in r.get_input_ids():
            if i == 9:
                r.get_node_by_id(i).set_label(newCarry)
                continue
            if turn:
                r.get_node_by_id(i).set_label(a[j])
                turn = False
            else:
                r.get_node_by_id(i).set_label(b[j])
                turn = True
            if turn:
                j += 1

        return newCarry, r

    @classmethod
    def half_adder(cls, a, b):
        """
        :param a, b: registre de taille 2**n
        :return: bit de retenue, registre de taille 2**n qui contient la somme de a et b modulo 2**n
        """
        return cls.adder(a, b, 0)

    @classmethod
    def int_to_boolcirc(cls, n):
        taille = 0
        p = n
        if n > 255:
            while p > 1:
                p //= 2
                taille += 1
        else:
            taille = 8
        binary = bin(n)[2:]
        binary = "0" * (taille - len(binary)) + binary
        r = bool_circ(open_digraph())
        for new_node in binary:
            new_node_id = r.new_id()
            r.add_node(new_node)
            r.add_node(label="", parents={new_node_id: 1})
        return r

    def copies(self, *ids):
        for i in ids:
            node_i = self.get_node_by_id(i)
            print(node_i.get_children_ids())
            if len(node_i.get_children_ids()) == 0:
                self.remove_node_by_id(i)
                continue
            node_children_id = self.get_node_by_id(list(node_i.get_children_ids().keys())[0])
            for keys in node_children_id.get_children_ids():
                self.add_node(label=node_i.get_label(),children={keys: 1})
            self.remove_node_by_id(node_i.get_id(), node_children_id.get_id())

    def porte_Non(self, *ids):
        for i in ids:
            node_i = self.get_node_by_id(i)

            if len(node_i.get_children_ids()) == 0:
                self.remove_node_by_id(i)
                continue
            node_children_id = self.get_node_by_id(list(node_i.get_children_ids().keys())[0])
            s = "0" if node_i.get_label() == "1" else "1"
            for keys in node_children_id.get_children_ids():
                self.add_node(label=s, children={keys: 1})
            self.remove_node_by_id(node_i.get_id(), node_children_id.get_id())

    def porte_Et(self, *ids):
        for i in ids:
            node_i = self.get_node_by_id(i)
            if node_i.get_label() != "1":
                for keys in node_i.get_parent_ids():
                    self.add_node(label="", parents={keys: 1})
                # On le fait dans element neutre
                for keys in node_i.get_children_ids():
                    self.get_node_by_id(keys).set_label("0")
                    # self.add_node(label="0", children={keys: 1})
            self.remove_node_by_id(i)

    def porte_Ou(self, *ids):
        for i in ids:
            node_i = self.get_node_by_id(i)
            if node_i.get_label() != "0":
                for keys in node_i.get_parent_ids():
                    self.add_node("", parents={keys: 1})
                # On le fait dans element neutre
                for keys in node_i.get_children_ids():
                    self.get_node_by_id(keys).set_label("1")
            self.remove_node_by_id(i)

    def porte_Ou_Exculsif(self, *ids):
        for i in ids:
            node_i = self.get_node_by_id(i)
            if node_i.get_label() != "0":
                for keys in node_i.get_children_ids():
                    for keys2 in list(self.get_node_by_id(keys).get_children_ids()):
                        self.add_node(label="~", parents={keys: 1}, children={keys2: 1})
                        self.remove_parallel_edges((keys, keys2))
            self.remove_node_by_id(node_i.get_id())

    def element_Neutre(self, *ids):
        for i in ids:
            node_i = self.get_node_by_id(i)
            label = node_i.get_label()
            if label == "|" or label == "^":
                node_i.set_label("0")
            else:
                node_i.set_label("1")

    def evaluate(self):
        while True:
            # Je sais pas si c'est plus clair comme ca car on peut combiner les 2
            inputNode = [node for node in self.get_nodes()
                         if len(node.get_parent_ids()) == 0
                         and len(node.get_children_ids()) != 0]
            condition = [all(x in self.get_output_ids()
                          for x in node.get_children_ids())
                      for node in inputNode]
            if all(condition):
                break
            print(f"{inputNode =}")
            print(f"{self.get_output_ids()}")
            for i, currentNode in enumerate(inputNode):
                if not condition[i]:
                    if len(currentNode.get_children_ids()) == 0:
                        self.remove_node_by_id(currentNode.get_id())
                        continue
                    currentNodeChildId = list(currentNode.get_children_ids().keys())[0]
                    print(f'{currentNodeChildId =}')
                    print(f"{self.get_node_by_id(currentNodeChildId) =}")
                    currentNodeChild = self.get_node_by_id(currentNodeChildId)
                    print(f"{currentNodeChild.get_label()}")
                    # Si on les met tous dans des tableau et que on les transforme apres est ce que c plus efficace
                    if currentNode.get_label() != "0" and currentNode.get_label() != "1":
                        self.element_Neutre(currentNode.get_id())
                    elif currentNodeChild.get_label() == "^":
                        self.porte_Ou_Exculsif(currentNode.get_id())
                    elif currentNodeChild.get_label() == "~":
                        self.porte_Non(currentNode.get_id())
                    elif currentNodeChild.get_label() == "&":
                        self.porte_Et(currentNode.get_id())
                    elif currentNodeChild.get_label() == "|":
                        self.porte_Ou(currentNode.get_id())
                    else:
                        self.copies(currentNode.get_id())
        inputNode = [node for node in self.get_nodes()
                     if len(node.get_parent_ids()) == 0
                     and len(node.get_children_ids()) != 0]
        print(inputNode)
        for node in inputNode:
            if node.get_label() != "1" and node.get_label() != "0":
                self.element_Neutre(node.get_id())
