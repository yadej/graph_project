import webbrowser
from modules import open_digraph


# noinspection PyUnresolvedReferences
class open_digraph_dot_mx:

    def digraph_to_string(self, arg1, *args):
        """
        inputs : arg1: args:
        outputs : string (str)
        """
        string = ""
        # k = list(arg1.get_children_ids().keys())
        Targ = list(args)
        # for a in args:
        #   if a.get_id() in k:
        #         k.remove(a.get_id())
        #    k = [x for x in k if x not in a.get_children_ids()]
        # for i in range(len(k)):
        m = Targ[-1].get_children_ids()
        if len(m) == 1:
            b = list(m.keys())
            p = (*args, self.get_node_by_id(b[0]))
            self.remove_edge((Targ[-1].get_id(), b[0]))
            string = string + self.digraph_to_string(arg1, *p)
            return string
        string = string + f'v{arg1.get_id()}'
        # Targ = list(args)
        for arg in range(len(Targ)):
            # self.remove_edge((arg1.get_id(),Targ[arg].get_id()))
            string = string + f' -> v{Targ[arg].get_id()}'
            if arg == 0:
                self.remove_edge((arg1.get_id(), Targ[0].get_id()))
        string = string + ';\n'
        return string

    def save_as_dot_file(self, path, verbose=False):
        """
        inputs : path (str)
        outputs : verbose (bool)
        enregistrer en fichier .dot par ex:

        digraph G {
        v0 [label="&"];
        v1 [label="~"];
        v4 [label="|"];
        v0 -> v1 -> v2;
        v0 -> v3;
        v2 -> v3;
        v2 -> v3;
        v3 -> v4;
        v2 -> v4;
        }
        """
        newOp = self.copy()
        with open(path, 'w+') as f:
            p = 'digraph G { \n'
            for i in newOp.get_nodes():
                if i.get_label() != '':
                    p += f'v{i.get_id()} [label="'
                    if verbose:
                        p += f'v{i.get_id()}: '
                    p += f'{i.get_label()}"]; \n'
            for n in newOp.get_nodes():
                for i in list(n.get_children_ids().keys()):
                    for j in range(n.get_children_ids().get(i)):
                        p += newOp.digraph_to_string(n, newOp.get_node_by_id(i))
            p += '}'
            f.write(p)

    @classmethod
    def from_dot_file(cls, path, verbose=False):
        """
        inputs : path (str), verbose (bool)
        outputs : graph (open_digraph)
        return un digraph lu dans un fichier .dot
        """
        graph = open_digraph.open_digraph()

        with open(path, 'r') as f:
            for line in f.readlines():
                if line[0] == 'v':
                    if line[3] == "[":
                        if verbose:
                            newlabel = line[4]
                            a = 5
                            while len(graph.get_node_ids()) < int(line[1]):
                                graph.add_node()
                            while line[a] != "]":
                                newlabel = newlabel + line[a]
                                a = a + 1
                            graph.add_node(label=newlabel)
                    else:
                        c = 1
                        while line[c] != ';':
                            if c % 6 == 1 and c > 6:
                                while (graph.new_id()) < int(line[c]) + 1:
                                    graph.add_node()

                            c += 1
                        while c > 2:
                            graph.add_edge((int(line[(c - 6) - 1]), int(line[c - 1])))
                            c = c - 6
        return graph

    def display(self, verbose=False):
        """
        inputs : verbose (bool)
        outputs : none
        affiche directement le graphe
        """
        self.save_as_dot_file('tmp.dot', verbose)
        f = open("./tmp.dot", 'r')
        txt = f.readlines()
        newTxt = '%0A%09'
        for line in txt[1:-1]:
            line = line[:-1]
            if line[4] != 'l' or not verbose:
                # NewLine = line.split(' -> ')
                # line = '->'.join(NewLine)
                newTxt = newTxt + line + '%0A%09'
            else:
                # NewLine =line.split('"')
                # line = '%3D\"'.join(NewLine[0:1]) + "\"]%5D%3B%0D%0A"
                newTxt = newTxt + line  # + '%0A%09'
        url = f'https://dreampuf.github.io/GraphvizOnline/#digraph{"{" + newTxt + "}"}'
        webbrowser.open(url)
