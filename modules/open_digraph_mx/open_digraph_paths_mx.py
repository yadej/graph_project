# noinspection PyUnresolvedReferences
class open_digraph_paths_mx:

    def dijkstra(self, src, direction=None, tgt=None):
        """
        inputs : src(int), direction({None , 1 ,-1}) tgt(int)
        outputs : dist(dict of int), prev(dict of int)
        return a dict of distance compared with src and a dict with the previous one as key
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
            else:
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
        inputs : src(int), tgt(int)
        outputs : int
        return the distance between src and tgt

        """

        dist, prev = self.dijkstra(src, tgt=tgt)
        return dist[tgt]

    def common_ancestor(self, src1, src2):
        """
        inputs : src1(int), src2(int)
        outputs : dict of tuple of int
        return  a dictionary of the distance of the of src and tgt

        """
        dist1, prev1 = self.dijkstra(src1, direction=-1)
        dist2, prev2 = self.dijkstra(src2, direction=-1)

        p = list(set(dist1) & set(dist2))
        m = {}
        for a in p:
            m[a] = (dist1[a], dist2[a])
        return m

    def tri_topologique(self):
        """
        inputs : None
        outputs : list of list of int
        return  a list of id_node layer by layer

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
                if i not in visited and len(k.get_node_by_id(i).get_children_ids()) == 0 and len(
                        k.get_node_by_id(i).get_parent_ids()) == 0:
                    nb += 1
                    visited.append(i)
        # C'est pour ajoute la derniere ligne
        flat_old = [item for t in old for item in t]
        p = [i for i in k.get_node_ids() if i not in flat_old]
        old.append(p)
        return old

    def noeuds_profondeur(self, i):
        """
        inputs : id(int)
        outputs : int
        return  the depth of the node of id
        """
        a = self.tri_topologique()
        for depth in range(len(a)):
            if i in a[depth]:
                return depth
        # Return -1 si le noeud n'est pas dans le digraph
        return -1

    def prof_OpD(self):
        """
        inputs : None
        outputs : int
        return  max layer of digraph
        """
        a = self.tri_topologique()
        if a:
            return len(a) - 1
        else:
            return 0

    def max_dist(self, src, tgt):
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
        if id1p > id2p:
            dico = {src: 0}
            last = tgt
        else:
            dico = {tgt: 0}
            last = src
            id1p, id2p = id2p, id1p
        prev = {}
        for i in range(id1p, id2p, -1):
            for j in T[i - 1]:
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
