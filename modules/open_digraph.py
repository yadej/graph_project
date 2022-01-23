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

    # getters node
    def get_id(self):
        return self.id

    def get_label(self):
        return self.label

    def get_parents_id(self):
        return self.parents

    def get_children_id(self):
        return self.children

    # setters node
    def set_id(self, id2):
            self.id = id2

    def set_label(self, label2):
            self.label = label2

    def set_parents_ids(self, par2):
            self.parents = par2

    def set_children_ids(self, ch2):
            self.children = ch2
            
    def add_child_id(self,id2):
            self.children.append(id2)
        
    def add_parent_id(self,id2):
            self.children.append(id2)
    # copy function
    def copy(self):
        self = copy.copy(self)


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

    # getters open_digraph
    def get_input_ids(self):
        return self.inputs

    def get_output_ids(self):
        return self.outputs
    
    def get_id_node_map(self):
        return self.nodes
    
    def get_nodes(self):
        return self.nodes.values()
    
    def get_node_ids(self):
        return [i.get_id for i in self.nodes.values() ]
    
    #setters open_diagraph
    def set_input_ids(self,id2):
        self.inputs = id2
        
    def set_output_ids(self,id2):
        self.outputs = id2
        
    def add_input_id(self,id2):
        self.inputs.append(id2)
        
    def add_output_id(self,id2):
        self.outputs.append(id2)
    
    def copy(self):
        self = copy.copy(self)
        
    def new_id(self):
        k = self.get_node_ids().sorted()
        p = 1
        m = 0
        while true:
            if k[m] == p:
                m,p = m + 1, p + 1
            else:
                break
        return p
    
    def add_edge(self, src, tgt):
        pass
        
    @classmethod
    def empty(cls):
        return cls(0,0, {})
