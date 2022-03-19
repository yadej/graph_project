import copy


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
        inputs : none
        outputs : id of node (int)
        returns id of the node
        """
        return self.id

    def get_label(self):
        """
        inputs : none
        outputs : label of node (string)
        returns label of the node
        """
        return self.label

    def get_parent_ids(self):
        """
        inputs : none
        outputs : parents id of node (int -> int dict)
        returns parent ids of the node
        """
        return self.parents

    def get_children_ids(self):
        """
        inputs : none
        outputs : childeren id of node (int -> int dict)
        returns children ids of the node
        """
        return self.children

    # setters
    def set_id(self, i):
        """
        inputs : id to set (int)
        outputs : none
        sets node id to i
        """
        self.id = i

    def set_label(self, label):
        """
        inputs : label to set (string)
        outputs : none
        sets node label to label
        """
        self.label = label

    def set_parent_ids(self, ids):
        """
        inputs : id to set (int)
        outputs : none
        sets node parent ids to ids
        """
        self.parents = ids

    def set_children_ids(self, ids):
        """
        inputs : id to set (int)
        outputs : none
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
        inputs : none
        output : copy of the node
        returns a copy of the node
        """
        return copy.deepcopy(self)

    def remove_parent_once(self, i):
        """
        input : id of open_digraph (int i)
        output : none (procedure)
        removes the parent of id i
        """
        self.parents[i] = self.parents.get(i, 0) - 1
        if self.parents[i] <= 0:
            self.parents.pop(i)

    def remove_child_once(self, i):
        """
        input : id of open_digraph
        output : none (procedure)
        removes the child of id i
        """
        self.children[i] = self.children.get(i, 0) - 1
        if self.children[i] <= 0:
            self.children.pop(i)

    def remove_parent_id(self, i):
        """
        inputs : id of open_digraph (int i)
        outputs : none (procedure)
        removes all occurences of parent of id i
        """
        self.parents[i] = 0
        self.parents.pop(i)

    def remove_child_id(self, i):
        """
        inputs : id of the open_digraph (int i)
        outputs : none
        removes all occurences of child of id
        """
        self.children[i] = 0
        self.children.pop(i)

    def indegree(self):
        """
        inputs : none (method)
        outputs : incoming degree of the open_digraph
        """
        return sum(self.get_parent_ids().values())

    def outdegree(self):
        """
        inputs : none
        outputs : outgoing degree of the open_digraph
        """
        return sum(self.get_children_ids().values())

    def degree(self):
        """
        inputs : none (method)
        outputs : total degree of the open_digraph (incoming + outcoming)
        """
        return self.indegree() + self.outdegree()
