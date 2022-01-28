import copy


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
        return f'identity: {self.id}, label: {self.label}, children: {self.children}'

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

    def add_child_id(self, i):
        '''
        adds node child id i
        '''
        self.children[i] = self.children.get(i, 0) + 1

    def add_parent_id(self, i):
        '''
        adds parent id i
        '''
        self.parents[i] = self.parents.get(i, 0) + 1

    def copy(self):
        '''
        returns a copy of the node
        '''
        return copy.copy(self)

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

    def __init__(self, inputs, outputs, nodes):
        '''
        inputs: int list; the ids of the input nodes
        outputs: int list; the ids of the output nodes
        nodes: node iter;
        '''
        self.inputs = inputs
        self.outputs = outputs
        self.nodes = {node.id: node for node in nodes}  # self.nodes: <int,node> dict

    def __str__(self):
        return f'inputs: {self.inputs}, outputs: {self.outputs}, nodes: {self.nodes}'

    def __repr__(self):
        return str(self)

    @classmethod
    def empty(cls):
        '''
        returns an empty graph
        '''
        return cls(0, 0, {})

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
        return self.nodes.values()

    def get_node_ids(self):
        '''
        returns a list of ids from every node in the graph
        '''
        return [i.get_id for i in self.nodes.values()]

    def get_node_by_id(self, i):
        '''
        returns the node corresponding to the id i
        '''
        return self.nodes[i]

    def get_nodes_by_ids(self, ids):
        '''
        returns a list of every node which id is in l
        '''
        return [self.nodes[i] for i in ids]

    # setters
    def set_input_ids(self, ids):
        '''
        sets input ids to ids
        '''
        self.inputs = ids

    # permet d'attribuer une nouvelle sortie au graphe
    def set_output_ids(self, ids):
        '''
        sets output ids to ids
        '''
        self.outputs = ids

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
        return copy.copy(self)

    def new_id(self):
        '''
        returns an unassigned id for the graph
        '''
        # On suppose que l'id 0 n'existe pas
        k = self.get_node_ids().sorted()
        p = 1
        m = 0
        while True:
            if k[m] == p:
                m, p = m + 1, p + 1
            else:
                break
        return p

    def add_edge(self, src, tgt):
        '''
        adds an edge from src to tgt
        '''
        self.get_node_by_id(src).add_child_id(tgt)
        self.get_node_by_id(tgt).add_parent_id(src)

    def add_node(self, label='', parents={}, children={}):
        '''
        adds a node to the graph
        '''
        k = self.new_id()
        self.nodes[k] = node(k, label, parents, children)
        for i in parents.keys():
            self.nodes[i].add_child_id(k)
        for i in children.keys():
            self.nodes[i].add_parent_id(k)

    def remove_edge(self, src, tgt):
        '''
        removes an edge from src to tgt
        '''
        self.get_node_by_id(src).remove_child_once(tgt)
        self.get_node_by_id(tgt).remove_parent_once(src)

    def remove_parallel_edges(self, src, tgt):
        '''
        removes any edge from src to tgt
        '''
        self.get_node_by_id(src).remove_child_id(tgt)
        self.get_node_by_id(tgt).remove_parent_id(src)

    def remove_node_by_id(self, i):
        '''
        removes node of id i
        '''
        # enleve tout les parents de i
        for k in self.get_node_by_id(i).get_parent_ids():
            self.get_node_by_id(k).remove_child_id(i)
            self.get_node_by_id(i).remove_parent_id(k)
        # enleve tout les enfants de i
        for k in self.get_node_by_id(i).get_child_ids():
            self.get_node_by_id(i).remove_child_id(k)
            self.get_node_by_id(k).remove_parent_id(i)

    def remove_edges(self, srcs, tgts):
        for src, tgt in srcs, tgts:
            self.remove_edge(src, tgt)

    def remove_parallel_edges_list(self, srcs, tgts):
        for src, tgt in srcs, tgts:
            self.remove_parallel_edges(src, tgt)

    def remove_nodes_by_id(self, ids):
        for i in ids:
            self.remove_node_by_id(i)

    def is_well_formed(self):
        '''
        returns true if the graph is well-formed else false
        '''
        for i, o in self.get_input_ids(), self.get_output_ids():
            # chaque noeud d’inputs et d’outputs doit etre dans le graphe (i.e. son id comme cĺef dans nodes)
            if not self.get_nodes().contains(i) or not self.get_nodes().contains(o):
                return False
            # chaque noeud input doit avoir un unique fils (de multiplicite 1) et pas de parent
            if self.get_node_by_id(i).get_parent_ids() != [] or self.get_node_by_id(i).get_children_ids().size() != 1:
                return False
            # chaque noeud output doit avoir un unique parent (de multiplicit ́e 1) et pas de fils
            if self.get_node_by_id(o).get_children_ids() != [] or self.get_node_by_id(o).get_parent_ids().size() != 1:
                return False
        # chaque clef de nodes pointe vers un noeud d’id la clef
        for clef in self.get_nodes():
            if clef not in clef.get_children_ids():
                return False
        # si j a pour fils i avec multiplicite m, alors i doit avoir pour parent j avec multip. m, et vice-versa
        ...
        return True

    def add_input_node(self, nodeId, label=''):
        '''
        adds an input node with id and label to the graph
        '''
        self.add_input_id(self.new_id())
        self.add_node(label, {}, {nodeId: 1})

    def add_output_node(self, nodeId, label=''):
        '''
        adds an output node with id and label to the graph
        '''
        self.add_output_id(self.new_id())
        self.add_node(label, {nodeId: 1}, {})
