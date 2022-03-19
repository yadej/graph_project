import random
from modules.adjacency_matrix import random_int_matrix, graph_from_adjacency_matrix


# noinspection PyUnresolvedReferences
class open_digraph_matrix_mx:
    @classmethod
    def random(cls, n, bound, inputs=0, outputs=0, form='free'):
        """
        inputs : inputs (int), outputs (int), form (string), (j'ai des doutes pour les autres)
        outputs : random graph (open_digraph)
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
        """
        inputs : none
        outputs : dictonary ids (int dict)
        return dictionary which associate node's ids with int 0 <= i < n
        """
        p = max(self.get_node_ids())
        dico = {}
        for i in range(p):
            dico[i] = random.randrange(p)
        return dico

    def adjacency_matrix(self):
        """
        inputs : none
        outputs : adjency matrix (matrix)
        returns graph's adjency matrix
        """
        p = len(self.get_node_ids())
        matrix = [[0 for _ in range(p)] for _ in range(p)]
        for i in self.get_nodes():
            for x, y in i.get_parent_ids().items():
                matrix[x][i.get_id()] = y
            for x, y in i.get_children_ids().items():
                matrix[i.get_id()][x] = y
        return matrix
