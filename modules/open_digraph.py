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
    # renvoie le node représenté par une chaîne de caractères.
    def __str__(self):
        return f'identity: {self.id}, label: {self.label}, children: {self.children}'
    # renvoie la chaîne de caractère utilisée pour afficher le noeud
    def __repr__(self):
        return str(self)

    # getters node
    # renvoie l'identifiant du node
    def get_id(self):
        return self.id
    # renvoie le label du node
    def get_label(self):
        return self.label
    # renvoie le parent du node
    def get_parent_ids(self):
        return self.parents
    # renvoie l'enfant du node
    def get_children_ids(self):
        return self.children

    # setters node
    # permet d'attriber un identifiant au node
    def set_id(self, i):
            self.id = i
    # permet d'attribuer un label au node
    def set_label(self, label):
            self.label = label
    # permet d'attriber un parent au node
    def set_parent_ids(self, p):
            self.parents = p
    # permet de définir un enfant pour le node
    def set_children_ids(self, c):
            self.children = c
    # permet d'ajouter un identifiant pour un enfant du noeud
    def add_child_id(self,i):
            self.children[i] = self.children.get(i,0)+ 1 
    # permet d'ajouter un identifiant pour un parent du noeud
    def add_parent_id(self,i):
            self.parents[i] = self.parents.get(i,0)+ 1 
    # copy function
    def copy(self):
        return copy.copy(self)
    #TD2exo1
    # supprime une occurende du parent correspondant à l'identifiant
    def remove_parent_once(self, i):
        
        self.parents[i] = self.parents.get(i,0) - 1
        if(self.parents[i] <=  0):
            self.parents.pop(i)

    # supprime une occurence de l'enfant correspondant à l'identifiant
    def remove_child_once(self, i):
        self.children[i] = self.children.get(i,0) - 1
        if(self.children[i] <=  0):
            self.children.pop(i)
    # supprime toutes les occurences de parent correspondant à l'identifiant
    def remove_parent_id(self, i):
        self.parents[i] = 0
        self.parents.pop(i)
    # supprime toutes les occurences de enfant correspondant à l'identifiant
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
    # renvoie le graphe représenté par une chaîne de caractères.
    def __str__(self):
        return f'inputs: {self.inputs}, outputs: {self.outputs}, nodes: {self.nodes}'
    # renvoie la chaîne de caractère utilisée pour afficher le graphe
    def __repr__(self):
         return str(self)
         
    @classmethod
    # retourne un graphe vide
    def empty(cls):
        return cls(0,0, {})

    # getters open_digraph
    # renvoie les entrées du graphe
    def get_input_ids(self):
        return self.inputs
    #renvoie les sorties du graphe
    def get_output_ids(self):
        return self.outputs
    # renvoie un dictionnaire contenant les noeuds par identifiants
    def get_id_node_map(self):
        return self.nodes
    # renvoie une liste de tous les noeuds du graphe
    def get_nodes(self):
        return self.nodes.values()
    # renvoie une liste des identifiants de tous les noeuds du graphe
    def get_node_ids(self):
        return [i.get_id for i in self.nodes.values()]
    # renvoie le noeud correspondant à l'identifiant
    def get_node_by_id(self, i):
        return self.nodes[i]
    # renvoie une liste des noeuds du graphe à partir d'une liste d'identifiants
    def get_nodes_by_ids(self, l):
        return [self.nodes[i] for i in l]
        
    #setters open_diagraph
    # permet d'attribuer une nouvelle entrée au graphe
    def set_input_ids(self,i):
        self.inputs = i
    # permet d'attribuer une nouvelle sortie au graphe
    def set_output_ids(self,i):
        self.outputs = i
    # permet d'ajouter une nouvelle entrée au graphe
    def add_input_id(self,i):
        self.inputs.append(i)
    # permet d'ajouter une nouvelle sortie au graphe
    def add_output_id(self,i):
        self.outputs.append(i)
    # retourne une copie du graphe
    def copy(self):
        return copy.copy(self)
    # renvoie un id non utilisé dans le graphe
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
    # Permet d'ajouter une arête du noeud d'id tgt au noeud d'id src
    def add_edge(self, src, tgt):
        
      
        self.get_node_by_id(src).add_child_id(tgt)
        self.get_node_by_id(tgt).add_child_id(src)
    # ajoute un noeud avec label au graphe (en utilisant un nouvel id)
    # le lie avec les noeuds d'ids parents et children (avec leur multiplicités respectives)
    def add_node(self, label='', parents={},children={}):
        k = self.new_id()
        self.nodes[k] = node(k,label,parents,children)
        for i in parents.keys():
            self.nodes[i].add_child_id(k)
        for i in children.keys():
            self.nodes[i].add_parent_id(k)
        
    #TD2exo2
    # supprime une arête de src vers tgt
    def remove_edge(self, src, tgt):
        self.get_node_by_id(src).remove_child_id(tgt)
        self.get_node_by_id(tgt).remove_parent_once(src)
    # supprime toutes les arêtes de src vers tgt
    def remove_parallel_edges(self, src, tgt):
        for i,j in src,tgt:
            self.remove_edge(i, j)
    # supprime toutes les arêtes associées au noeud
    def remove_node_by_id(self):
        pass
    #TD2exo3
    # vérifie si un graphe est bien formé. L'accepte dans ce cas et le rejette dans l'autre
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
    # crée un nouveau noeud que l'on place en entrée, et qui pointe vers le noeud dont on a donné l'id en paramètre
    def add_input_node(self):
        pass

    # crée un nouveau noeud que l'on place en sortie, et qui pointe vers le noeud dont on a donné l'id en paramètre
    def add_output_node(self):
        pass
