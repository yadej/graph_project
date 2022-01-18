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


        def get_id(self):
            return self.id

        def get_label(self):
            return self.label

        def get_parents_id(self):
            return self.parents

        def get_children_id(self):
            return self.children


class open_digraph:  # for open directed graph

    def __init__(self, inputs, outputs, nodes):
        '''
        inputs: int list; the ids of the input nodes
        outputs: int list; the ids of the output nodes
        nodes: node iter;
        '''
        self.inputs = inputs
        self.outputs = outputs
        self.nodes = {node.id:node for node in nodes} # self.nodes: <int,node> dict

        def get_input_ids(self):
            return self.inputs

        def get_output_ids(self):
            return self.outputs
        
    def __str__(self):
        return f'inputs: {self.inputs}, outputs: {self.outputs}, nodes: {self.nodes}'
