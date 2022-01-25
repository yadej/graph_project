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
            self.children[i] = self.children.get(i,0)+ 1 
        
    def add_parent_id(self,i):
            self.parents[i] = self.parents.get(i,0)+ 1 
    # copy function
    def copy(self):
        return copy.copy(self)
    #TD2exo1
    def remove_parent_once(self, i):
        
        self.parents[i] = self.parents.get(i,0) - 1
        if(self.parents[i] <=  0):
            self.parents.pop(i)
    
    def remove_child_once(self, i):
        self.children[i] = self.children.get(i,0) - 1
        if(self.children[i] <=  0):
            self.children.pop(i)
    
    def remove_parent_id(self, i):
        self.parents[i] = 0
        self.parents.pop(i)
    
    def remove_child_id(self, i):
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
        # On suppose que l'id 0 n'existe pas
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
        
      
        self.get_node_by_id(src).add_child_id(tgt)
        self.get_node_by_id(tgt).add_child_id(src)
            
    def add_node(self, label='', parents={},children={}):
        k = self.new_id()
        self.nodes[k] = node(k,label,parents,children)
        for i in parents.keys():
            self.nodes[i].add_child_id(k)
        for i in children.keys():
            self.nodes[i].add_parent_id(k)
        
    #TD2exo2
    def remove_edge(self, src, tgt):
        self.get_node_by_id(src).remove_child_id(tgt)
        self.get_node_by_id(tgt).remove_parent_once(src)

    def remove_parallel_edges(self, src, tgt):
        for i,j in src,tgt:
            self.remove_edge(i, j)

    def remove_node_by_id(self):
        pass
    #TD2exo3
    def is_well_formed(self):
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
            # chaque cĺe de nodes pointe vers un noeud d’id la clef
            if not clef.get_children_ids().contains(clef)
                return False
            # si j a pour fils i avec multiplicite m, alors i doit avoir pour parent j avec multiplicite m, et vice-versa
        
    def add_input_node(self):
        pass
            
        
