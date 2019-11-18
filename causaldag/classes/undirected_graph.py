from collections import defaultdict
from copy import deepcopy
import numpy as np
# from cvxopt import spmatrix


class UndirectedGraph:
    def __init__(self, nodes=set(), edges=set()):
        self._nodes = set(nodes)
        self._edges = {frozenset({i, j}) for i, j in edges}
        self._neighbors = defaultdict(set)
        self._degrees = defaultdict(int)
        for i, j in self._edges:
            self._nodes.add(i)
            self._nodes.add(j)
            self._neighbors[i].add(j)
            self._neighbors[j].add(i)
            self._degrees[i] += 1
            self._degrees[j] += 1

    def __eq__(self, other):
        return self._nodes == other._nodes and self._edges == other._edges

    def to_amat(self, node_list=None, sparse=False) -> np.ndarray:
        """
        Return an adjacency matrix for this undirected graph.

        Parameters
        ----------
        node_list:
            List indexing the rows/columns of the matrix.

        Return
        ------
        amat

        Examples
        --------
        TODO
        """
        if not node_list:
            node_list = sorted(self._nodes)
        node2ix = {node: i for i, node in enumerate(node_list)}

        if sparse:
            raise NotImplementedError
            # js, ks = [], []
            # for j, k in self._edges:
            #     js.append(j)
            #     ks.append(k)
            #     js.append(k)
            #     ks.append(j)
            # return spmatrix(1, js, ks)
        amat = np.zeros([self.num_nodes, self.num_nodes], dtype=int)

        for i, j in self._edges:
            amat[node2ix[i], node2ix[j]] = True
            amat[node2ix[j], node2ix[i]] = True
        return amat

    @classmethod
    def from_amat(self, amat):
        """
        Return an undirected graph with edges given by amat, i.e. i-j if amat[i,j] != 0

        Parameters
        ----------
        amat:
            Numpy matrix representing edges in the undirected graph.

        Examples
        --------
        >>> amat = np.array([[0, 0, 1], [0, 1, 0], [0, 0, 0]])
        >>> cd.UndirectedGraph.from_amat(amat)
        TODO
        """
        edges = {(i, j) for (i, j), val in np.ndenumerate(amat) if val != 0}
        return UndirectedGraph(nodes=set(range(amat.shape[0])), edges=edges)

    def copy(self, new=True):
        """
        Return a copy of this undirected graph.
        """
        return UndirectedGraph(self._nodes, self._edges)

    @property
    def num_nodes(self) -> int:
        return len(self._nodes)

    @property
    def num_edges(self) -> int:
        return len(self._edges)

    @property
    def degrees(self):
        return {node: self._degrees[node] for node in self._nodes}

    @property
    def neighbors(self):
        return {node: self._neighbors[node] for node in self._nodes}

    @property
    def edges(self) -> set:
        return self._edges.copy()

    @property
    def nodes(self) -> set:
        return self._nodes.copy()

    @property
    def skeleton(self) -> set:
        return self.edges

    def has_edge(self, i, j) -> bool:
        """
        Check if the undirected graph has an edge.

        Parameters
        ----------
        i:
            first endpoint of edge.
        j:
            second endpoint of edge.

        Examples
        --------
        TODO
        """
        return frozenset({i, j}) in self._edges

    def neighbors_of(self, node) -> set:
        """
        Return the neighbors of a node.

        Parameters
        ----------
        node

        Examples
        --------
        TODO
        """
        return self._neighbors[node].copy()

    # === MUTATORS ===
    def add_edge(self, i, j):
        """
        Add an edge.

        Parameters
        ----------
        i:
            first endpoint of edge to be added.
        j:
            second endpoint of edge to be added.

        See Also
        --------
        add_edges_from
        delete_edge

        Examples
        --------
        TODO
        """
        if frozenset({i, j}) not in self._edges:
            self._edges.add(frozenset({i, j}))
            self._neighbors[i].add(j)
            self._neighbors[j].add(i)
            self._degrees[i] += 1
            self._degrees[j] += 1

    def add_edges_from(self, edges):
        """
        Add a set of edges.

        Parameters
        ----------
        edges:
            Edges to be added.

        See Also
        --------
        add_edge
        delete_edges_from

        Examples
        --------
        TODO
        """
        for i, j in edges:
            self.add_edge(i, j)

    def delete_edges_from(self, edges):
        """
        Delete a set of edges.

        Parameters
        ----------
        edges:
            Edges to be deleted.

        See Also
        --------
        add_edges_from
        delete_edge

        Examples
        --------
        TODO
        """
        for i, j in edges:
            self.delete_edge(i, j)

    def delete_edge(self, i, j):
        """
        Delete an edge.

        Parameters
        ----------
        i:
            first endpoint of edge to be deleted.
        j:
            second endpoint of edge to be deleted.

        See Also
        --------
        add_edge
        delete_edges_from

        Examples
        --------
        TODO
        """
        self._edges.remove(frozenset({i, j}))
        self._neighbors[i].remove(j)
        self._neighbors[j].remove(i)
        self._degrees[i] -= 1
        self._degrees[j] -= 1

    def delete_node(self, i):
        """
        Delete a node.

        Parameters
        ----------
        TODO

        Examples
        --------
        TODO
        """
        self._nodes.remove(i)
        for j in self._neighbors[i]:
            self._neighbors[j].remove(i)
            self._degrees[j] -= 1
            self._edges.remove(frozenset({i, j}))
        self._neighbors.pop(i, None)
        self._degrees.pop(i, None)

