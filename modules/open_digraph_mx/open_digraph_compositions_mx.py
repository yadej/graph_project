class open_digraph_compositions_mx:

    def min_id(self):
        return min(list(self.get_node_ids()))

    def max_id(self):
        return max(list(self.get_node_ids()))

    def shift_indices(self, n):
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

    def connected_components(self):
        ...

    def list(self):
        ...
