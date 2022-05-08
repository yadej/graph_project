# noinspection PyUnresolvedReferences
class open_digraph_paths_mx:

    def dijkstra(self, src, direction=None, tgt=None):
        """
        :param src: id of source node
        :param direction: None by default (for both ways),
        1 (descending only), -1 (ascending only)
        :param tgt: optional id of target node
        :return: dict of distance to source node,
        and dict with previous node as key
        """
        if self.get_node_by_id(src) == 0:
            raise Exception('not in digraph')

        Q = [src]
        dist = {src: 0}
        prev = {}

        while Q:
            u = min(Q, key=lambda x: dist[x])
            Q.remove(u)

            if u == tgt:
                return dist, prev

            v = []

            if direction is None:
                v = v + list(self.get_node_by_id(u).get_children_ids().keys()) + list(self.get_node_by_id(
                    u).get_parent_ids().keys())

            elif direction == 1:
                v = v + list(self.get_node_by_id(u).get_children_ids().keys())

            else:  # direction == -1
                v = v + list(self.get_node_by_id(u).get_parent_ids().keys())

            for i in v:
                if i not in dist:
                    Q.append(i)

                if i not in dist or dist[i] > dist[u] == 1:
                    dist[i] = dist[u] + 1
                    prev[i] = u

        return dist, prev

    def shortest_path(self, src, tgt):
        """
        :param src: id of the source node
        :param tgt: id of the target node
        :return: list of node ids from src to tgt
        """
        d = self.dijkstra(src, tgt=tgt)
        i = tgt
        path = [i]

        while i != src:
            i = d[1][i]
            path = [i] + path

        return path

    def common_ancestors(self, src1, src2):
        """
        :param src1: id of the first source node
        :param src2: id of the second source node
        :return: dictionary of every common ancestor of the source nodes,
        and their distance to both source nodes
        """
        dist1 = self.dijkstra(src1, direction=-1)[0]
        dist2 = self.dijkstra(src2, direction=-1)[0]
        return {a: (dist1[a], dist2[a]) for a in dist1.keys() & dist2.keys()}

    def tri_topologique(self):
        """
        :return: list of lists of node ids that correspond to every layer in the graph from top to bottom
        """
        g = self.copy()
        layers = []
        visited = []
        nb = 0

        while nb != len(g.get_nodes()):
            new = []

            # on met les les noeuds qui ont enfants mais pas parents dans new
            for i in g.get_node_ids():
                if not g.get_node_by_id(i).get_parent_ids() \
                        and g.get_node_by_id(i).get_children_ids():
                    new.append(i)
            print(new)
            print(g)
            if not new:
                raise Exception("the graph is cyclic")

            # on enleve les enfants de ces noeuds
            for i in new:
                for a in list(g.get_node_by_id(i).get_children_ids()):
                    g.remove_parallel_edges((i, a))

            # on a la couche qu'on cherchait
            layers.append(new)

            for i in g.get_node_ids():
                if i not in visited \
                        and not g.get_node_by_id(i).get_parent_ids() \
                        and not g.get_node_by_id(i).get_children_ids():
                    nb += 1
                    visited.append(i)

        # ajouter la derniere ligne
        flat_old = [n for layer in layers for n in layer]
        p = [i for i in g.get_node_ids() if i not in flat_old]
        layers.append(p)
        return layers

    def node_depth(self, i):
        """
        :param i: node id
        :return: depth of the node in the graph
        """
        for depth, node_ids in enumerate(self.tri_topologique()):
            if i in node_ids:
                return depth

        return -1  # node not in graph

    def depth(self):
        """
        :return: max depth of digraph
        """
        return len(self.tri_topologique())

    def max_dist(self, u, v):
        """
        :param u: id of the source node
        :param v: id of the target node
        :return: maximum distance between source and target nodes
        """
        u_depth, v_depth = self.node_depth(u), self.node_depth(v)

        if u_depth == -1:
            raise Exception('u is not in the graph')
        if v_depth == -1:
            raise Exception('v is not in the graph')

        if u_depth > v_depth:
            u, v = v, u
            u_depth, v_depth = v_depth, u_depth
        dico = {u: 0}
        last = v

        prev = {}
        T = self.tri_topologique()

        for depth in range(u_depth, v_depth):
            for i in T[depth + 1]:
                inter = dico.keys() & self.get_node_by_id(i).get_parent_ids()
                if inter:
                    p = max(inter, key=lambda x: dico[x])
                    dico[i] = dico[p] + 1
                    prev[i] = p

        i = last
        path = [i]

        while i != u:
            i = prev[i]
            path = [i] + path

        return max(dico[u], dico[v]), path
