"""
A weighted directed graph implementation in pure python.

Graphs have nodes connected by edges. The edges have a "weight" attached to
them. We use a combination of a hashmap and direct map to keep track of
arbitrary hashable node values and their corresponding natural number id.

We implement the following interface:
set_edge(u: any, v: any, w: float) -> None : sets weight w from node u to v.
get_edge(u: any, v: any) -> float : gets weight w from node u to v.
get_outdegree(u: any) -> int : gets number of nodes pointing from u.

To keep track of the nodes and edges, we use an adjacency list implementation.
This scheme works best when the graph is relatively sparse. For every node,
we have a list of outgoing edges, which are stored as pairs of [target, weight].
Unfortunately, this makes get_indegree quite slow as we have to search
all the other adjacency lists, so we do not implement it.
"""
from copy import deepcopy

class Wdgraph:
    def __init__(self):
        self.len = 0
        self.hashmap = {}
        self.directmap = []
        self.adj_list = []

    def register_node(self, u):
        """
        Given some node value, return the natural number associated with it.
        Register the node if it is not found.
        """
        if u in self.hashmap: return self.hashmap[u]
        self.hashmap[u] = self.len
        self.directmap.append(u)
        self.len += 1
        self.adj_list.append([])
        return self.len - 1

    def map_value(self, u):
        """
        Given some node value, return the natural number associated with it.
        Raise an exception if the node value is not found.
        """
        if u in self.hashmap: return self.hashmap[u]
        raise Exception("Trying to access unregistered node value")

    def raw_set_edge(self, n1, n2, w):
        for source, (target, weight) in enumerate(self.adj_list[n1]):
            if target == n2:
                self.adj_list[n1][source][1] = w
                return

        self.adj_list[n1].append([n2, w])

    def set_edge(self, u, v, w):
        n1 = self.register_node(u)
        n2 = self.register_node(v)

        self.raw_set_edge(n1, n2, w)

    def get_edge(self, u, v):
        n1 = self.map_value(u)
        n2 = self.map_value(v)

        for target, weight in self.adj_list[n1]:
             if target == n2:
                 return weight

        raise Exception(f"No edge exists between {u} and {v}")

    def all_edges(self):
        return [edge for edges in self.adj_list for edge in edges]

    def remove_edge(self, u, v):
        n1 = self.map_value(u)
        n2 = self.map_value(v)

        to_remove = None

        for target, weight in self.adj_list[n1]:
             if target == n2:
                 to_remove = [target, weight]

        if to_remove is not None:
            self.adj_list[n1].remove(to_remove)
            return

        raise Exception(f"No edge exists between {u} and {v}")

    def get_outdegree(self, u):
        n = self.map_value(u)
        return len(self.adj_list[n])

    def get_outneighbors(self, u):
        """
        Get the neighbors that are pointing out from node u.
        Returned as a list of [target, weight] pairs.
        """
        n = self.map_value(u)
        return [[self.directmap[target], weight] for target, weight in self.adj_list[n]]

    def get_inneighbors(self, u):
        n = self.map_value(u)

        inneighbors = []

        for m, outs in enumerate(self.adj_list):
            for target, weight in outs:
                if target == n:
                    inneighbors.append([self.directmap[m], weight])

        return inneighbors

    def create_probability_graph(self):
        """
        Converts the graph into a markov chain that shows probability of moving
        from one node to another, if weights are frequencies.
        """
        for source in range(len(self.adj_list)):
            total = sum([weight for target, weight in self.adj_list[source]])
            for target, weight in self.adj_list[source]:
                self.raw_set_edge(source, target, weight / total)

    def get_nodes(self):
        return self.directmap

    def get_edges(self):
        edges = []

        for edge in self.adj_list:
            edges.append([[self.directmap[node], weight] for node, weight in edge])

        return edges

    def get_nodes_without_incoming(self):
        all_nodes = set(self.directmap)
        with_incoming = set()

        for edge in self.adj_list:
            for node, weight in edge:
                with_incoming.add(self.directmap[node])

        return all_nodes - with_incoming

    def copy(self):
        new_graph = Wdgraph()

        new_graph.len = self.len
        new_graph.hashmap = deepcopy(self.hashmap)
        new_graph.directmap = deepcopy(self.directmap)
        new_graph.adj_list = deepcopy(self.adj_list)

        return new_graph

    def __len__(self):
        return self.len
