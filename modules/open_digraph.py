import copy
import random

from modules.adjacency_matrix import random_int_matrix, graph_from_adjacency_matrix
from modules.open_digraph_mx.open_digraph_compositions_mx import open_digraph_compositions_mx
from modules.open_digraph_mx.open_digraph_dot_mx import open_digraph_dot_mx


class node:

    def __init__(self, identity, label, parents, children):
        """
        identity: int; its unique id in the graph
        label: string;
        parents: int->int dict; maps a parent node's id to its multiplicity
        children: int->int dict; maps a child node's id to its multiplicity
        """
        self.id = identity
        self.label = label
        self.parents = parents
        self.children = children

    def __str__(self):
        return f'(id: {self.id}, label: \'{self.label}\', parents: {self.parents}, children: {self.children})'

    def __repr__(self):
        return str(self)

    # getters
    def get_id(self):
        """
        returns id of the node
        """
        return self.id

    def get_label(self):
        """
        returns label of the node
        """
        return self.label

    def get_parent_ids(self):
        """
        returns parent ids of the node
        """
        return self.parents

    def get_children_ids(self):
        """
        returns children ids of the node
        """
        return self.children

    # setters
    def set_id(self, i):
        """
        sets node id to i
        """
        self.id = i

    def set_label(self, label):
        """
        sets node label to label
        """
        self.label = label

    def set_parent_ids(self, ids):
        """
        sets node parent ids to ids
        """
        self.parents = ids

    def set_children_ids(self, ids):
        """
        sets node children ids to ids
        """
        self.children = ids

    # features
    def add_child_id(self, i, n=1):
        """
        adds node child id i
        """
        self.children[i] = self.children.get(i, 0) + n

    def add_parent_id(self, i, n=1):
        """
        adds parent id i n times
        """
        self.parents[i] = self.parents.get(i, 0) + n

    def copy(self):
        """
        returns a copy of the node
        """
        return copy.deepcopy(self)

    def remove_parent_once(self, i):
        """
        removes the parent of id i
        """
        self.parents[i] = self.parents.get(i, 0) - 1
        if self.parents[i] <= 0:
            self.parents.pop(i)

    def remove_child_once(self, i):
        """
        removes the child of id i
        """
        self.children[i] = self.children.get(i, 0) - 1
        if self.children[i] <= 0:
            self.children.pop(i)

    def remove_parent_id(self, i):
        """
        removes all occurences of parent of id i
        """
        self.parents[i] = 0
        self.parents.pop(i)

    def remove_child_id(self, i):
        """
        removes all occurences of child of id i
        """
        self.children[i] = 0
        self.children.pop(i)

    def indegree(self):
        return sum(self.get_parent_ids().values())

    def outdegree(self):
        return sum(self.get_children_ids().values())

    def degree(self):
        return self.indegree() + self.outdegree()


class open_digraph(open_digraph_dot_mx, open_digraph_compositions_mx):

    def __init__(self, inputs=None, outputs=None, nodes=None):
        """
        inputs: int list; the ids of the input nodes
        outputs: int list; the ids of the output nodes
        nodes: node iter;
        """
        if nodes is None:
            nodes = {}
        if outputs is None:
            outputs = []
        if inputs is None:
            inputs = []
        self.inputs = inputs
        self.outputs = outputs
        self.nodes = {n.id: n for n in nodes}  # self.nodes: <int,node> dict

    def __str__(self):
        return f'(inputs: {self.inputs}, outputs: {self.outputs}, nodes: {self.nodes})'

    def __repr__(self):
        return str(self)

    @classmethod
    def empty(cls):
        """
        returns an empty graph
        """
        return cls([], [], {})

    # getters
    def get_input_ids(self):
        """
        returns the ids of input nodes
        """
        return self.inputs

    def get_output_ids(self):
        """
        returns the ids of output nodes
        """
        return self.outputs

    def get_id_node_map(self):
        """
        returns a dictionary containing the ids associated to their nodes
        """
        return self.nodes

    def get_nodes(self):
        """
        returns a list of every node in the graph
        """
        return self.get_id_node_map().values()

    def get_node_ids(self):
        """
        returns a list of ids from every node in the graph
        """
        return self.get_id_node_map().keys()

    def get_node_by_id(self, i):
        """
        returns the node corresponding to the id i
        """
        return self.nodes.get(i)

    def get_nodes_by_ids(self, ids):
        """
        returns a list of every node which id is in ids
        """
        return [self.get_node_by_id(i) for i in ids]

    # setters
    def set_input_ids(self, ids):
        """
        sets input ids to ids
        """
        self.inputs = ids

    def set_output_ids(self, ids):
        """
        sets output ids to ids
        """
        self.outputs = ids

    # features
    def add_input_id(self, i):
        """
        adds an input id i to the graph
        """
        self.inputs.append(i)

    def add_output_id(self, i):
        """
        adds an output id i to the graph
        """
        self.outputs.append(i)

    def copy(self):
        """
        returns a copy of the graph
        """
        return copy.deepcopy(self)

    def new_id(self):
        """
        returns an unassigned id for the graph
        """
        # l'id 0 est reservee pour les id par default ie. invalide
        m = 0
        for i in sorted(self.get_node_ids()):
            if i == m:
                m = m + 1
        return m

    def add_edge(self, *pairs):
        """
        adds an edge from src to tgt
        """
        for src, tgt in pairs:
            n_src = self.get_node_by_id(src)
            n_tgt = self.get_node_by_id(tgt)
            if n_src is not None and n_tgt is not None:
                n_src.add_child_id(tgt)
                n_tgt.add_parent_id(src)

    def add_node(self, label='', parents=None, children=None):
        """
        adds a node to the graph
        """
        if children is None:
            children = {}
        if parents is None:
            parents = {}
        k = self.new_id()
        self.nodes[k] = node(k, label, parents, children)
        for i, j in parents.items():
            self.nodes[i].add_child_id(k, j)
        for i, j in children.items():
            self.nodes[i].add_parent_id(k, j)

    def remove_edge(self, *pairs):
        """
        removes edges from src to tgt
        """
        for src, tgt in pairs:
            self.get_node_by_id(src).remove_child_once(tgt)
            self.get_node_by_id(tgt).remove_parent_once(src)

    def remove_parallel_edges(self, *pairs):
        """
        removes any edge from src to tgt
        """
        for src, tgt in pairs:
            self.get_node_by_id(src).remove_child_id(tgt)
            self.get_node_by_id(tgt).remove_parent_id(src)

    def remove_node_by_id(self, *ids):
        """
        removes node of id i
        """
        for i in ids:
            # enleve tout les parents de i
            for k in self.get_node_by_id(i).get_parent_ids():
                self.get_node_by_id(k).remove_child_id(i)
            self.get_node_by_id(i).get_parent_ids().clear()
            # enleve tout les enfants de i
            for k in self.get_node_by_id(i).get_children_ids():
                self.get_node_by_id(k).remove_parent_id(i)
            self.get_node_by_id(i).get_children_ids().clear()
            # self.get_id_node_map().pop(i)
            if i in self.get_input_ids():
                self.get_input_ids().remove(i)
            if i in self.get_output_ids():
                self.get_output_ids().remove(i)

    def is_well_formed(self):
        """
        returns true if the graph is well-formed else false
        """
        # chaque noeud d’inputs et d’outputs doit etre dans le graphe (i.e. son id comme clef dans nodes)
        for i in self.get_input_ids():
            if not self.get_node_by_id(i):
                return False
        for i in self.get_output_ids():
            if not self.get_node_by_id(i):
                return False
        # chaque noeud input doit avoir un unique fils (de multiplicite 1) et pas de parent
        for i in self.get_input_ids():
            if len(self.get_node_by_id(i).get_children_ids()) == 1 and self.get_node_by_id(i).get_parent_ids() == {}:
                continue
            else:
                return False

        # chaque noeud output doit avoir un unique parent (de multiplicite 1) et pas de fils
        for o in self.get_output_ids():
            if len(self.get_node_by_id(o).get_parent_ids()) == 1 and self.get_node_by_id(o).get_children_ids() == {}:
                continue
            else:
                return False

        # chaque clef de nodes pointe vers un noeud d’id la clef
        for k in self.get_node_ids():
            if self.get_id_node_map().get(k).get_id() != k:
                return False

        # si j a pour fils i avec multiplicite m, alors i doit avoir pour parent j avec multip. m, et vice-versa
        for j in self.get_nodes():
            for i in j.get_children_ids().keys():
                if j.get_children_ids().get(i) != self.get_node_by_id(i).get_parent_ids().get(j.get_id()):
                    return False
        return True

    def add_input_node(self, nodeId, label=''):
        """
        adds an input node to the graph that is pointing towards a node of id nodeId
        """
        if self.get_node_by_id(nodeId) in self.get_input_ids():
            raise Exception('node of argument nodeId is an input node')
        self.add_input_id(self.new_id())
        self.add_node(label, {}, {nodeId: 1})

    def add_output_node(self, nodeId, label=''):
        """
        adds an output node to the graph that is pointed by a node of id nodeId
        """
        if self.get_node_by_id(nodeId) in self.get_output_ids():
            raise Exception('node of argument nodeId is an output node')
        self.add_output_id(self.new_id())
        self.add_node(label, {nodeId: 1}, {})

    @classmethod
    def random(cls, n, bound, inputs=0, outputs=0, form='free'):
        """
        form: 'free' or 'DAG' or 'oriented' or loop-free' or 'undirected' or 'loop-free undirected'
        """
        if form == 'free':
            matrix = random_int_matrix(n, bound, null_diag=False, symetric=False, oriented=False, triangular=False)

        elif form == 'DAG':
            matrix = random_int_matrix(n, bound, null_diag=False, symetric=False, oriented=False, triangular=True)

        elif form == 'oriented':
            matrix = random_int_matrix(n, bound, null_diag=False, symetric=False, oriented=True, triangular=False)

        elif form == 'loop-free':
            matrix = random_int_matrix(n, bound, null_diag=True, symetric=False, oriented=False, triangular=False)

        elif form == 'undirected':
            matrix = random_int_matrix(n, bound, null_diag=False, symetric=True, oriented=False, triangular=True)

        elif form == 'loop-free undirected':
            matrix = random_int_matrix(n, bound, null_diag=True, symetric=False, oriented=False, triangular=True)
        else:
            raise Exception('not a valid open_digraph form')

        k = []
        for i in range(inputs):
            r = random.randrange(n)
            while r in k:
                r = random.randrange(n)
            k.append(r)

        p = []
        for i in range(outputs):
            r = random.randrange(n)
            while r in k or r in p:
                r = random.randrange(n)
            p.append(r)

        lastNode = list(range(n))
        print(k + p)
        for a in (p + k):
            for b in range(n):
                matrix[a][b] = 0
                matrix[b][a] = 0
            lastNode.remove(a)
        for i in k:
            newChild = random.randrange(len(lastNode))
            matrix[i][lastNode[newChild]] = 1
        for i in p:
            newParent = random.randrange(len(lastNode))
            matrix[lastNode[newParent]][i] = 1
        graph = graph_from_adjacency_matrix(matrix)
        graph.set_input_ids(k)
        graph.set_output_ids(p)
        return graph

    def dict_unique_id(self):
        p = max(self.get_node_ids())
        dico = {}
        for i in range(p):
            dico[i] = random.randrange(p)
        return dico

    def adjacency_matrix(self):
        p = len(self.get_node_ids())
        matrix = [[0 for _ in range(p)] for _ in range(p)]
        for i in self.get_nodes():
            for x, y in i.get_parent_ids().items():
                matrix[x][i.get_id()] = y
            for x, y in i.get_children_ids().items():
                matrix[i.get_id()][x] = y
        return matrix

    """def cyclic(self, visited=None):
        # pas de noeud -> acyclique
        if visited is None:
            visited = []
        if len(visited) == len(self.get_nodes()):
            return False
        # cherchons une feuille
        for n in self.get_nodes():
            if not n.get_id() in visited:
                if any(True for e in n.get_children_ids().keys() if e in visited):
                    return True
                else:
                    # on la retire et on recommence
                    self.remove_node_by_id(n.get_id())
                    visited.append(n.get_id())
                    return self.cyclic(visited)
                # if not list(n.get_children_ids().values()):  # si c'est une feuille
                # on la retire et on recommence
                # self.remove_node_by_id(n.get_id())
                # self.get_id_node_map().pop(n.get_id())
                # return self.cyclic()
        # si il n'y a pas de feuille -> cyclique
        return True """
    """
    def is_cyclic(self):
        if not self.get_nodes():
            return False
        k = self.copy()
        return k.cyclic()
    """

    def cyclic(self, v, visited, recStack):

        # Mark current node as visited and
        # adds to recursion stack
        visited[v] = True
        recStack[v] = True

        # Recur for all neighbours
        # if any neighbour is visited and in
        # recStack then graph is cyclic
        if self.get_node_by_id(v) is None:
            return False
        for n in self.get_node_by_id(v).get_children_ids().keys():
            if not visited[n]:
                if self.cyclic(n, visited, recStack):
                    return True
            elif recStack[n]:
                return True

        # The node needs to be poped from
        # recursion stack before function ends
        recStack[v] = False
        return False

    # Returns true if graph is cyclic else false
    def is_cyclic(self):
        visited = [False] * (len(self.get_nodes()) + 1)
        recStack = [False] * (len(self.get_nodes()) + 1)
        for n in self.get_nodes():
            if not visited[n.get_id()]:
                if self.cyclic(n.get_id(), visited, recStack):
                    return True
        return False

    def list(self):
        n, data = self.connected_components()
        dic = []
        for i in range(n):
            p = [self.get_node_by_id(key) for key in data.keys() if data[key] == i]
            dic.append(open_digraph(nodes=p))
        return dic

    def dijkstra(self, src, direction=None):
        Q = [src]
        dist = {src:0}
        prev = {}
        while Q:
            u = Q[0]
            for i,j in dist.items():
                if dist[u] > j:
                    u = i.get_id()
            Q.pop(u)
            v = []
            if direction is None:
                v = v + self.get_node_by_id(u).get_children_ids().keys() + self.get_node_by_id(u).get_parent_ids().keys()
            elif direction == 1:
                v = v + self.get_node_by_id(u).get_children_ids().keys()
            else:
                v = v + self.get_node_by_id(u).get_parent_ids().keys()
            for i in v:
                if not i in dist:
                    Q.append(i)
                if not i in dist or dist[i] > dist[u] = 1:
                    dist[v] = dist[u] + 1
                    prev[v] = u
        return dist, prev

class bool_circ(open_digraph):

    def __init__(self, g=None):
        if isinstance(g, open_digraph):
            super().__init__(g.get_input_ids(), g.get_output_ids(), g.get_nodes())
        if not g.is_well_formed():
            raise Exception('is not a boolean circuit')

    def is_well_formed(self):
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
