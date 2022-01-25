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

    def get_parent_ids(self):
        return self.parents

    def get_children_ids(self):
        return self.children

    # setters node
    def set_id(self, i):
            self.id = i

    def set_label(self, label):
            self.label = label

    def set_parent_ids(self, p):
            self.parents = p

    def set_children_ids(self, c):
            self.children = c
            
    def add_child_id(self,i):
            self.children.append(i)
        
    def add_parent_id(self,i):
            self.parents.append(i)
    # copy function
    def copy(self):
        return copy.copy(self)
    #TD2exo1
    def remove_parent_once(self, i):
        self.get_parent_ids.pop(i)
    
    def remove_child_once(self, i):
        self.get_children_ids.pop(i)
    
    def remove_parent_id(self, i):
        pass
    
    def remove_child_id(self, i):
        pass


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
        return cls(0,0, {})

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
        return [i.get_id for i in self.nodes.values()]
        
    def get_node_by_id(self, i):
        return self.nodes[i]
        
    def get_nodes_by_ids(self, l):
        return [self.nodes[i] for i in l]
        
    #setters open_diagraph
    def set_input_ids(self,i):
        self.inputs = i
        
    def set_output_ids(self,i):
        self.outputs = i
        
    def add_input_id(self,i):
        self.inputs.append(i)
        
    def add_output_id(self,i):
        self.outputs.append(i)
    
    def copy(self):
        return copy.copy(self)
        
    def new_id(self):
        k = self.get_node_ids().sorted()
        p = 1
        m = 0
        while True:
            if k[m] == p:
                m,p = m + 1, p + 1
            else:
                break
        return p
    
    def add_edge(self, src, tgt):
        pass
        

    def add_node(self, label='', parents=, children=):
        pass
    #TD2exo2
    def remove_edge(self, src, tgt):
        self.pop(tgt, src)
        return self

    def remove_parallel_edges(self, src, tgt):
        while True:
            self.remove_edge(src, tgt)

    def remove_node_by_id(self):
        pass
    #TD2exo3
    def is_well_formed(self):
        for i in self.get_output_ids:
            if not self.get_nodes().contains(i)
            or self.get_node_by_id(i).get_children_ids() != []
            or self.get_node_by_id(i).get_parent_ids().size() != 1:
                return False
        for i in self.get_input_ids:
            if not self.get_nodes().contains(i)
            or self.get_node_by_id(i).get_parent_ids() != []
            or self.get_node_by_id(i).get_children_ids().size() != 1:
                return False
        for clef in self.get_nodes():
            if not clef.get_parent_ids().contains(clef)
            or not 
                return False
        return True
        
