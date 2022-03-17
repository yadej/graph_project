# noinspection PyUnresolvedReferences
class open_digraph_compositions_mx:

    nodes: dict

    def min_id(self):
        """
        inputs : none
        outputs : min id of graph's nodes (int)
        """
        return min(list(self.get_node_ids()))

    def max_id(self):
        """
        inputs : none
        outputs : max id of graph's nodes (int)
        """
        return max(list(self.get_node_ids()))

    def shift_indices(self, n):
        """
        inputs : n (int)
        outputs : none
        adds n to all the indices of the graph.
        """
        for i in self.get_nodes():
            i.set_id(i.get_id() + n)
            k = {}
            for ci, m in i.get_children_ids().items():
                k[ci + n] = m
            i.set_children_ids(k)
            p = {}
            for ci, m in i.get_parent_ids().items():
                p[ci + n] = m
            i.set_parent_ids(p)
        ns = {}
        for i in self.get_nodes():
            ns[i.get_id() + n] = i
        self.nodes = ns
        self.set_input_ids([i + n for i in self.get_input_ids()])
        self.set_output_ids([i + n for i in self.get_output_ids()])

    def iparallel(self, *gs):
        """
        inputs : gs: list of open_digraph
        outputs ; none
        adds g to the open_digraph
        """
        for g in gs:
            self.shift_indices(g.max_id() - self.min_id() + 1)
            ns = {}
            for n in self.get_nodes():
                ns[n.get_id()] = n
            for n in g.get_nodes():
                ns[n.get_id()] = n
            self.set_input_ids(self.get_input_ids() + g.get_input_ids)
            self.set_output_ids(self.get_output_ids() + g.get_output_ids)
            self.nodes = ns

    def parallel(self, *gs):
        """
        inputs : gs: list of open_digraph
        outputs : k, parallel composition of the two graphs
        """
        k = self.copy()
        for g in gs:
            k.shift_indices(g.max_id() - k.min_id() + 1)
            ns = k.get_nodes()
            for n in g.get_nodes():
                ns[n.get_id()] = n
            k.get_input_ids().append(g.get_input_ids)
            k.get_output_ids().append(g.get_output_ids)
            k.nodes = ns
        return k

    def icompose(self, g):
        """
        inputs : g (open_digraph)
        outputs ; none
        makes the sequential composition of the two graphs.
        """
        if self.get_input_ids != g.get_output_ids:
            raise Exception('inputs do not match g outputs')
        self.shift_indices(g.max_id() - self.min_id() + 1)
        b1 = self.get_input_ids()
        b2 = g.get_output_ids()
        ns = {}
        for n in self.get_nodes():
            ns[n.get_id()] = n
        for n in g.get_nodes():
            ns[n.get_id()] = n
        self.set_input_ids(g.get_input_ids())
        self.nodes = ns
        for i, j in zip(b1, b2):
            self.add_edge((i, j))

    def compose(self, g):
        """
        inputs : g (open_digraph)
        outputs : k, composed of the two graphs
        """
        if self.get_input_ids != g.get_output_ids:
            raise Exception('inputs do not match g outputs')
        k = self.copy()
        k.shift_indices(g.max_id() - k.min_id() + 1)
        b1 = k.get_input_ids()
        b2 = g.get_output_ids()
        ns = {}
        for n in k.get_nodes():
            ns[n.get_id()] = n
        for n in g.get_nodes():
            ns[n.get_id()] = n
        k.set_input_ids(g.get_input_ids)
        k.set_output_ids(k.get_input_ids())
        k.nodes = ns
        for i, j in zip(b1, b2):
            k.add_edge((i, j))
        return k

    def is_connected(self, i, visited):
        """
        inputs : i : id of graph (int), visited : list of ids (int list)
        outputs : visited (int list)
        """
        visited.append(i)
        if not self.get_node_by_id(i).get_children_ids() in visited:
            for j in self.get_node_by_id(i).get_children_ids():
                if j not in visited:
                    visited = self.is_connected(j, visited)
        if not self.get_node_by_id(i).get_parent_ids() in visited:
            for j in self.get_node_by_id(i).get_parent_ids():
                if j not in visited:
                    visited = self.is_connected(j, visited)
        return visited

    def connected_components(self):
        """
        inputs : none
        outputs : nb : number of connected components, dic : dictionary which associate each ids to an integer
        corresponding to a connected component
        """
        nb = 0
        if len(self.get_nodes()) == 0:
            return nb
        visited = []
        dic = {}
        while len(visited) != len(self.get_nodes()):
            new_v = []
            for i in self.get_node_ids():
                if new_v:
                    break
                if i not in visited:
                    new_v = self.is_connected(i, new_v)
            visited = visited + new_v
            for i in new_v:
                dic[i] = nb
            nb += 1
        return nb, dic
