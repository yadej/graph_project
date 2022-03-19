import copy
from modules.node import node
from modules.open_digraph_mx.open_digraph_dot_mx import open_digraph_dot_mx
from modules.open_digraph_mx.open_digraph_compositions_mx import open_digraph_compositions_mx
from modules.open_digraph_mx.open_digraph_matrix_mx import open_digraph_matrix_mx
from modules.open_digraph_mx.open_digraph_paths_mx import open_digraph_paths_mx


class open_digraph(open_digraph_dot_mx, open_digraph_compositions_mx, open_digraph_matrix_mx, open_digraph_paths_mx):

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
        inputs : none
        outputs : empty graph (open_digraph)
        returns an empty graph
        """
        return cls([], [], {})

    # getters
    def get_input_ids(self):
        """
        inputs : none
        outputs : id op input notes (int)
        returns the ids of input nodes
        """
        return self.inputs

    def get_output_ids(self):
        """
        input : none
        outputs : id of output nodes (int)
        returns the ids of output nodes
        """
        return self.outputs

    def get_id_node_map(self):
        """
        input : none
        output : dictionary of id (int dict)
        returns a dictionary containing the ids associated to their nodes
        """
        return self.nodes

    def get_nodes(self):
        """
        input : none
        output : list of nodes (node list)
        returns a list of every node in the graph
        """
        return self.get_id_node_map().values()

    def get_node_ids(self):
        """
        inputs : none
        outputs : list of graph's nodes ids (int list)
        returns a list of ids from every node in the graph
        """
        return self.get_id_node_map().keys()

    def get_node_by_id(self, i):
        """
        input : id (int)
        output : node associated to the id (node)
        returns the node corresponding to the id i
        """
        return self.nodes.get(i)

    def get_nodes_by_ids(self, ids):
        """
        inputs : list of nodes' id (int list)
        outputs : list of nodes have id present in id list (node list)
        returns a list of every node which id is in ids
        """
        return [self.get_node_by_id(i) for i in ids]

    # setters
    def set_input_ids(self, ids):
        """
        inputs : list of ids (int list)
        outputs : none
        sets input ids to ids
        """
        self.inputs = ids

    def set_output_ids(self, ids):
        """
        inputs : list of ids (int list)
        outputs : none
        sets output ids to ids
        """
        self.outputs = ids

    # features
    def add_input_id(self, i):
        """
        inputs : id (int)
        outputs : none
        adds an input id i to the graph
        """
        self.inputs.append(i)

    def add_output_id(self, i):
        """
        inputs : id (int)
        outputs : none
        adds an output id i to the graph
        """
        self.outputs.append(i)

    def copy(self):
        """
        input : none
        outputs : copy of graph (graph)
        returns a copy of the graph
        """
        return copy.deepcopy(self)

    def new_id(self):
        """
        input : non
        outputs : id (int)
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
        inputs : list of ids (int list)
        outputs : none
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
        inputs : label (string), parents id (int), children id (int)
        outputs : none
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
        inputs : list of ids (int list)
        outputs : none
        removes edges from src to tgt
        """
        for src, tgt in pairs:
            self.get_node_by_id(src).remove_child_once(tgt)
            self.get_node_by_id(tgt).remove_parent_once(src)

    def remove_parallel_edges(self, *pairs):
        """
        inputs : list of ids (int list)
        outputs : none
        removes any edge from src to tgt
        """
        for src, tgt in pairs:
            self.get_node_by_id(src).remove_child_id(tgt)
            self.get_node_by_id(tgt).remove_parent_id(src)

    def remove_node_by_id(self, *ids):
        """
        inputs : list of ids (int list)
        outputs : none
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
        inputs : none
        outputs : boolean (bool)
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
        inputs : node id (int), label (string)
        outputs : none
        adds an input node to the graph that is pointing towards a node of id nodeId
        """
        if self.get_node_by_id(nodeId) in self.get_input_ids():
            raise Exception('node of argument nodeId is an input node')
        self.add_input_id(self.new_id())
        self.add_node(label, {}, {nodeId: 1})

    def add_output_node(self, nodeId, label=''):
        """
        inputs : node id (int), label (string)
        outputs : none
        adds an output node to the graph that is pointed by a node of id nodeId
        """
        if self.get_node_by_id(nodeId) in self.get_output_ids():
            raise Exception('node of argument nodeId is an output node')
        self.add_output_id(self.new_id())
        self.add_node(label, {nodeId: 1}, {})
