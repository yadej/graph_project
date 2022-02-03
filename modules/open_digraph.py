import copy
import random
import modules.matrice

class node:

    def __init__(self, identity, label, parents, children):
        '''
        identity: int; its unique id in the graph
        label: string;
        parents: int->int dict; maps a parent node's id to its multiplicity
        children: int->int dict; maps a child node's id to its multiplicity
        '''
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
        '''
        returns id of the node
        '''
        return self.id

    def get_label(self):
        '''
        returns label of the node
        '''
        return self.label

    def get_parent_ids(self):
        '''
        returns parent ids of the node
        '''
        return self.parents

    def get_children_ids(self):
        '''
        returns children ids of the node
        '''
        return self.children

    # setters
    def set_id(self, i):
        '''
        sets node id to i
        '''
        self.id = i

    def set_label(self, label):
        '''
        sets node label to label
        '''
        self.label = label

    def set_parent_ids(self, ids):
        '''
        sets node parent ids to ids
        '''
        self.parents = ids

    def set_children_ids(self, ids):
        '''
        sets node children ids to ids
        '''
        self.children = ids

    # features
    def add_child_id(self, i, n=1):
        '''
        adds node child id i
        '''
        self.children[i] = self.children.get(i, 0) + n

    def add_parent_id(self, i, n=1):
        '''
        adds parent id i n times
        '''
        self.parents[i] = self.parents.get(i, 0) + n

    def copy(self):
        '''
        returns a copy of the node
        '''
        return copy.deepcopy(self)

    def remove_parent_once(self, i):
        '''
        removes the parent of id i
        '''
        self.parents[i] = self.parents.get(i, 0) - 1
        if self.parents[i] <= 0:
            self.parents.pop(i)

    def remove_child_once(self, i):
        '''
        removes the child of id i
        '''
        self.children[i] = self.children.get(i, 0) - 1
        if self.children[i] <= 0:
            self.children.pop(i)

    def remove_parent_id(self, i):
        '''
        removes all occurences of parent of id i
        '''
        self.parents[i] = 0
        self.parents.pop(i)

    def remove_child_id(self, i):
        '''
        removes all occurences of child of id i
        '''
        self.children[i] = 0
        self.children.pop(i)


class open_digraph:  # for open directed graph

    def __init__(self, inputs=[], outputs=[], nodes={}):
        '''
        inputs: int list; the ids of the input nodes
        outputs: int list; the ids of the output nodes
        nodes: node iter;
        '''
        self.inputs = inputs
        self.outputs = outputs
        self.nodes = {n.id: n for n in nodes}  # self.nodes: <int,node> dict

    def __str__(self):
        return f'(inputs: {self.inputs}, outputs: {self.outputs}, nodes: {self.nodes})'

    def __repr__(self):
        return str(self)

    @classmethod
    def empty(cls):
        '''
        returns an empty graph
        '''
        return cls([], [], {})

    # getters
    def get_input_ids(self):
        '''
        returns the ids of input nodes
        '''
        return self.inputs

    def get_output_ids(self):
        '''
        returns the ids of output nodes
        '''
        return self.outputs

    def get_id_node_map(self):
        '''
        returns a dictionary containing the ids associated to their nodes
        '''
        return self.nodes

    def get_nodes(self):
        '''
        returns a list of every node in the graph
        '''
        return self.get_id_node_map().values()

    def get_node_ids(self):
        '''
        returns a list of ids from every node in the graph
        '''
        return self.get_id_node_map().keys()

    def get_node_by_id(self, i):
        '''
        returns the node corresponding to the id i
        '''
        return self.nodes.get(i, 0)

    def get_nodes_by_ids(self, ids):
        '''
        returns a list of every node which id is in ids
        '''
        return [self.get_node_by_id(i) for i in ids]

    # setters
    def set_input_ids(self, ids):
        '''
        sets input ids to ids
        '''
        self.inputs = ids

    def set_output_ids(self, ids):
        '''
        sets output ids to ids
        '''
        self.outputs = ids

    # features
    def add_input_id(self, i):
        '''
        adds an input id i to the graph
        '''
        self.inputs.append(i)

    def add_output_id(self, i):
        '''
        adds an output id i to the graph
        '''
        self.outputs.append(i)

    def copy(self):
        '''
        returns a copy of the graph
        '''
        return copy.deepcopy(self)

    def new_id(self):
        '''
        returns an unassigned id for the graph
        '''
        # l'id 0 est reservee pour les id par default ie. invalide
        m = 0
        for i in sorted(self.get_node_ids()):
            if i == m:
                m = m + 1
        return m

    def add_edge(self, *pairs):
        '''
        adds an edge from src to tgt
        '''
        for src, tgt in pairs:
            self.get_node_by_id(src).add_child_id(tgt)
            self.get_node_by_id(tgt).add_parent_id(src)

    def add_node(self, label='', parents={}, children={}):
        '''
        adds a node to the graph
        '''
        k = self.new_id()
        self.nodes[k] = node(k, label, parents.copy(), children.copy())
        for i, j in parents.items():
            self.nodes[i].add_child_id(k, j)
        for i, j in children.items():
            self.nodes[i].add_parent_id(k, j)

    def remove_edge(self, *pairs):
        '''
        removes edges from src to tgt
        '''
        for src, tgt in pairs:
            self.get_node_by_id(src).remove_child_once(tgt)
            self.get_node_by_id(tgt).remove_parent_once(src)

    def remove_parallel_edges(self, *pairs):
        '''
        removes any edge from src to tgt
        '''
        for src, tgt in pairs:
            self.get_node_by_id(src).remove_child_id(tgt)
            self.get_node_by_id(tgt).remove_parent_id(src)

    def remove_node_by_id(self, *ids):
        '''
        removes node of id i
        '''
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
        '''
        returns true if the graph is well-formed else false
        '''
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
        '''
        adds an input node to the graph that is pointing towards a node of id nodeId
        '''
        if self.get_node_by_id(nodeId) in self.get_input_ids():
            raise Exception('node of argument nodeId is an input node')
        self.add_input_id(self.new_id())
        self.add_node(label, {}, {nodeId: 1})

    def add_output_node(self, nodeId, label=''):
        '''
        adds an output node to the graph that is pointed by a node of id nodeId
        '''
        if self.get_node_by_id(nodeId) in self.get_output_ids():
            raise Exception('node of argument nodeId is an output node')
        self.add_output_id(self.new_id())
        self.add_node(label, {nodeId: 1}, {})

    @classmethod
    def random(cls, n, bound, inputs=0, outputs=0, form='free'):
        '''
        form: 'free' or 'DAG' or 'oriented' or loop-free' or 'undirected' or 'loop-free undirected'
        '''
        if form=='free':
            m = modules.matrice.random_int_matrix(n, bound, null_diag=False, symetric=False, oriented=False, triangular=False)
            
        elif form=='DAG':
            m = modules.matrice.random_int_matrix(n, bound, null_diag=False, symetric=False, oriented=False, triangular=True)
            
        elif form=='oriented':
            m = modules.matrice.random_int_matrix(n, bound, null_diag=False, symetric=False, oriented=True, triangular=False)
            
        elif form=='loop-free':
            m = modules.matrice.random_int_matrix(n, bound, null_diag=True, symetric=False, oriented=False, triangular=False)
            
        elif form=='undirected':
            m = modules.matrice.random_int_matrix(n, bound, null_diag=False, symetric=True, oriented=False, triangular=True)
        
        elif form=='loop-free undirected':
            m = modules.matrice.random_int_matrix(n, bound, null_diag=True, symetric=False, oriented=False, triangular=True)
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
        LastNode = list(range(n))
        print( k + p)
        for a in (p + k ):
            for b in range(n):
                m[a][b] = 0
                m[b][a] = 0
            LastNode.remove(a)
        for i in k:
            NewChild = random.randrange(len(LastNode))
            m[i][LastNode[NewChild]] = 1
        for i in p:
            NewParent = random.randrange(len(LastNode))
            m[LastNode[NewParent]][i] = 1
        Mat = modules.matrice.graph_from_adjacency_matrix(m)
        Mat.set_input_ids(k)
        Mat.set_output_ids(p)
        return Mat
    def dict_unique_id(self):
        p = max(self.get_node_ids())
        dict = {}
        for i in range(p):
            dict[i] = random.randrange(p)
        return dict
