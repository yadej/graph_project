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
        :return: distance between the source node and target node
        """
        return self.dijkstra(src, tgt=tgt)[0][tgt]

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
        :return: list of node ids for every layer in the graph
        """
        k = self.copy()
        old = []
        visited = []
        nb = 0

        while nb != len(k.get_nodes()):
            new = []

            for i in k.get_node_ids():
                if len(k.get_node_by_id(i).get_children_ids()) == 0 and len(k.get_node_by_id(i).get_parent_ids()) != 0:
                    new.append(i)

            if not new:
                raise Exception("Digraph cyclic")

            for i in new:
                for a in list(k.get_node_by_id(i).get_parent_ids()):
                    k.remove_parallel_edges((a, i))

            old.append(new)
            for i in k.get_node_ids():
                if i not in visited \
                        and len(k.get_node_by_id(i).get_children_ids()) == 0 \
                        and len(k.get_node_by_id(i).get_parent_ids()) == 0:
                    nb += 1
                    visited.append(i)

        # C'est pour ajouter la derniere ligne
        flat_old = [item for t in old for item in t]
        p = [i for i in k.get_node_ids() if i not in flat_old]
        old.append(p)
        #Retourne l'inverse d'old
        return old[::-1]

    def node_depth(self, i):
        """
        :param i: node id
        :return: depth of the node in the graph
        """
        a = self.tri_topologique()

        for depth in range(len(a)):
            if i in a[depth]:
                return depth

        return -1  # node not in graph

    def prof_OpD(self):
        """
        :return: max depth of digraph
        """
        return len(self.tri_topologique())

    def max_dist(self, src, tgt):
        """
        :param src: id of the source node
        :param tgt: id of the target node
        :return: maximum distance between source and target nodes
        """
        a = list(self.get_node_ids())
        if src not in a or tgt not in a:
            raise Exception("Noeud qui ne sont pas dans le graph")
        T = self.tri_topologique()
        id1p = 0
        id2p = 0
        for i in range(len(T)):
            if src in T[i]:
                id1p = i
            if tgt in T[i]:
                id2p = i
        if id1p < id2p:
            dico = {src: 0}
            last = tgt
        else:
            dico = {tgt: 0}
            last = src
            id1p, id2p = id2p, id1p
        prev = {}
        for i in range(id1p, id2p):
            for j in T[i + 1]:
                v1 = set(self.get_node_by_id(j).get_parent_ids())
                v2 = set(dico.keys())
                v3 = list(v1 & v2)
                if v3:
                    p = max(v3, key=lambda x: dico[x])
                    dico[j] = dico[p] + 1
                    prev[j] = p
        newprev = {}
        if last == tgt:
            while last != src:
                newprev[last] = prev[last]
                last = prev[last]
        else:
            while last != tgt:
                newprev[last] = prev[last]
                last = prev[last]
        return max(dico[src], dico[tgt]), newprev
