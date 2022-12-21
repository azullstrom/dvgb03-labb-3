#!/usr/bin/env python3

import sys
import logging

log = logging.getLogger(__name__)

from math import inf

class AdjacencyList:
    '''
    A linked-list implementation of an adjacency list that keeps its nodes and
    edges lexicographically ordered at all times.
    '''
    def __init__(self, name=None, info=None):
        '''
        Initializes a new adjacency list.  It is considered empty if no head
        node is provided.  Optionally, a node can also have associated info.
        '''
        self._name = name # head node name
        self._info = info # head node info
        if not self.head().is_empty():
            self._tail = AdjacencyList() # empty tail
            self._edges = Edge() # empty list of edges

    def is_empty(self):
        '''
        Returns true if this adjacency list is empty.
        '''
        return self._name is None

    def head(self):
        '''
        Returns the head of this adjacency list.
        '''
        return self

    def tail(self):
        '''
        Returns the tail of this adjacency list.
        '''
        return self._tail

    def cons(self, tail):
        '''
        Returns the head of this adjacency list with a newly attached tail.
        '''
        self._tail = tail
        return self.head()

    def name(self):
        '''
        Returns the node name.
        '''
        return self._name

    def info(self):
        '''
        Returns auxilirary node info.
        Info is used for setting node distance and previous node in Dijkstra and Prim.
        Structure: [distance, previous]
        '''
        return self._info

    def edges(self):
        '''
        Returns the edge head.
        '''
        return self._edges

    def set_name(self, name):
        '''
        Sets the node name to `name`.

        Returns an adjacency list head.
        '''
        self._name = name
        return self.head()

    def set_info(self, info):
        '''
        Sets the auxilirary info of this node to `info`.
        Info is used for setting node distance and previous node in Dijkstra and Prim.
        Structure: [distance, previous]
        Returns an adjacency list head.
        '''
        self._info = info
        return self.head()

    def set_edges(self, edges):
        '''
        Sets the edge head of this node to `edges`.

        Returns an adjacency list head.
        '''
        self._edges = edges
        return self.head()

    ###
    # Node operations
    ###
    def add_node(self, name, info=None):
        '''
        Adds a new node named `name` in lexicographical order.  If node `name`
        is a member, its info-field is updated based on `info`.

        Returns an adjacency list head.
        '''
        if self.is_empty():
            return AdjacencyList(name, info)
        elif name < self.name():
            new_node = AdjacencyList(name, info)
            return new_node.cons(self.head())
        else:
            return self.cons(self.tail().add_node(name, info))

    def delete_node(self, name):
        '''
        Deletes the node named `name` if it is a member.

        Returns an adjacency list head.
        '''
        if self.is_empty():
            return self.head()
        elif name == self.name():
            return self.tail()
        elif name > self.name():
            self.cons(self.tail().delete_node(name))
        return self.head()

    def find_node(self, name):
        '''
        Returns True if the node named `name` is a member.
        '''
        if self.head().is_empty():
            return False
        if name == self.head().name():
            return True
        return self.tail().find_node(name)

    def get_node(self, name):
        '''
        ### HELP METHOD ###
        Returns a node if the node named `name` is a member.
        '''
        if self.head().is_empty():
            return 0
        if name == self.head().name():
            return self.head()
        return self.tail().get_node(name)

    def node_cardinality(self):
        '''
        Returns the number of nodes. Recursively moving the tail until
        the tail is empty. Then the recursion ends and the number of nodes is
        returned.
        '''
        if self.is_empty():
            return 0
        else:
            return self.tail().node_cardinality() + 1

    ###
    # Edge operations
    ###
    def add_edge(self, src, dst, weight=1):
        '''
        Adds or updates an edge from node `src` to node `dst` with a given
        weight `weight`.  If either of the two nodes are non-members, the same
        adjacency list is returned without any modification.

        Returns an adjacency list head.
        '''
        if not self.find_node(src) or not self.find_node(dst):
            return self.head()
        return self._add_edge(src, dst, weight)

    def _add_edge(self, src, dst, weight):
        '''
        Adds a new (or updates an existing) edge from node `src` to node `dst`,
        setting the weight to `weight`.

        Returns an adjacency list head.

        Pre: `dst` and 'src' is a member of this adjacency list.
        '''
        if src == self.name():
            self.set_edges(self.edges().add(dst, weight))
        elif src > self.name():
            self.tail()._add_edge(src, dst, weight)
        return self.head()

    def delete_edge(self, src, dst):
        '''
        Deletes an edge from node `src` to node `dst` if it exists.

        Returns an adjacency list head.
        '''
        if not self.find_edge(src, dst):
            return self.head()
        return self._delete_edge(src, dst)

    def _delete_edge(self, src, dst):
        '''
        Deletes an edge from node `src` to node `dst`.

        Returns an adjacency list head.
        '''
        if src == self.name():
            self.set_edges(self.edges().delete(dst))
        elif src > self.name():
            self.tail()._delete_edge(src, dst)
        return self.head()

    def delete_edges(self, name):
        '''
        Deletes all edges towards the node named `name`.

        Returns an adjacency list head.
        '''
        if not self.head().is_empty():
            self.set_edges(self.edges().delete(name))
            self.tail().delete_edges(name)
        return self.head()

    def find_edge(self, src, dst):
        '''
        Returns True if there's an edge from node `src` to node `dst`.
        '''
        if self.head().is_empty():
            return False
        elif src == self.name():
            return self.edges().find(dst)
        else:
            return self.tail().find_edge(src, dst)

    def edge_cardinality(self):
        '''
        Returns the number of edges.
        '''
        if self.head().is_empty():
            return 0
        else:
            return self.edges().cardinality() + self.tail().edge_cardinality()

    def self_loops(self):
        '''
        Returns the number of loops in this adjacency list.  Note that a loop is
        defined as a node that has an edge towards itself, e.g., A->A.
        '''
        if self.is_empty():
            return 0
        elif self.find_edge(self.name(), self.name()):
            return self.tail().self_loops() + 1
        else:
            return self.tail().self_loops()

    def adjacency_matrix(self):
        '''
        Returns this adjacency list as an adjacency matrix.  For example,
        consider the following adjacency list where all edges have weight=1.
        
        a: a->b->c
        |
        v
        b: a->b
        |
        v
        c: c

        Then we would expect the following 3x3 adjacency matrix:

          a b c
        -+-----
        a|1 1 1
        b|1 1 *
        c|* * 1

        Where the corresponding python-matrix is:

        [ [1,1,1], [1,1,inf], [inf,inf,1] ]

        Note that inf indicates that there is no path between two nodes.  Also,
        all rows and columns are lexicographically ordered based on node names.

        Hint: depending on your solution, you may need to add a helper method
        that maps a node's name to its numeric position in the adjacency list.
        '''
        if self.is_empty():
            return [[]]

        n = self.node_cardinality()
        matrix = [[inf] * n for i in range(n)]
        matrix = self.add_list_to_matrix(matrix)
        return matrix

    def add_list_to_matrix(self, matrix):
        '''
        ### HELP METHOD ###
        Takes a matrix with size of nodes * nodes filled with inf values.

        Returns an adjacency matrix with the edge weight between every dst node and the
        src node.
        '''
        current_node = self.head()

        i = 0
        while not current_node.is_empty():
            current_edge = current_node.edges()
            e = current_edge.cardinality()
            for j in range(e):
                if not current_edge.is_empty():
                    dst_index = self.find_dst_index(current_edge.dst())
                    matrix[i][dst_index] = current_edge.head().weight()
                current_edge = current_edge.tail()
            current_node = current_node.tail()
            i += 1
        return matrix

    def find_dst_index(self, dst):
        '''
        ### HELP METHOD ###
        Returns list index of a dst node by traversing the node list
        and increasing return number by 1 for each recursion until found.

        Pre: dst node exists.
        '''
        if dst == self.name():
            return 0
        else:
            return self.tail().find_dst_index(dst) + 1

    def list_nodes(self):
        '''
        Returns a list of node names in lexicographical order.
        '''
        head, node_names = self.head(), []
        while not head.is_empty():
            node_names += [ head.name() ]
            head = head.tail()
        return node_names

    def list_nodes_object(self):
        '''
        ### HELP METHOD ###
        Returns a list of nodes in lexicographical order.
        '''
        head, nodes = self.head(), []
        while not head.is_empty():
            nodes.append(head)
            head = head.tail()
        return nodes

    def list_edges(self):
        '''
        Returns a list of edges in lexicographical order.
        '''
        if self.head().is_empty():
            return []
        return self.head().edges().list(self.head().name()) +\
            self.tail().list_edges()

    def list_edges_object(self):
        '''
        ### HELP METHOD ###
        Returns a list of edges in lexicographical order.
        '''
        head, edges = self.head().edges(), []
        while not head.is_empty():
            edges.append(head)
            head = head.tail()
        return edges


class Edge:
    '''
    A linked-list implementation of edges that originate from an implicit source
    node.  Each edge has a weight and goes towards a given destination node.
    '''
    def __init__(self, dst=None, weight=1):
        '''
        Initializes a new edge sequence.  It is considered empty if no head edge
        is provided, i.e., dst is set to None.
        '''
        self._dst = dst # where is this edge's destination
        self._weight = weight # what is the weight of this edge
        if not self.head().is_empty():
            self._tail = Edge() # empty edge tail

    def is_empty(self):
        '''
        Returns true if this edge is empty.
        '''
        return self._dst is None
    
    def head(self):
        '''
        Returns the head of this edge.
        '''
        return self

    def tail(self):
        '''
        Returns the tail of this edge.
        '''
        return self._tail

    def cons(self, tail):
        '''
        Returns the head of this sequence with a newly attached tail.
        '''
        self._tail = tail
        return self.head()

    def dst(self):
        '''
        Returns the node name that this edge goes towards.
        '''
        return self._dst

    def weight(self):
        '''
        Returns the weight of this edge.
        '''
        return self._weight

    def set_dst(self, dst):
        '''
        Sets the destination of this edge to `dst`.

        Returns an edge head.
        '''
        self._dst = dst
        return self.head()

    def set_weight(self, weight):
        '''
        Sets the weight of this edge to `weight`.

        Returns an edge head.
        '''
        self._weight = weight
        return self.head()
    
    ###
    # Operations
    ###
    def add(self, dst, weight=1):
        '''
        Adds a new edge towards `dst` in lexicographical order.  If such an
        edge exists already, the associated weight-field is updated instead.

        Returns an edge head.
        '''
        if self.head().is_empty():
            return Edge(dst, weight)
        elif dst == self.dst():
            self.set_weight(weight)
            return self.head()
        elif dst < self.dst():
            new_edge = Edge(dst, weight)
            return new_edge.cons(self.head())
        else:
            return self.cons(self.tail().add(dst, weight))

    def delete(self, dst):
        '''
        Deletes the edge that goes towards `dst` if it exists.

        Returns an edge head.
        '''
        if self.is_empty():
            return self.head()
        elif dst == self.dst():
            return self.tail()
        else:
            return self.cons(self.tail().delete(dst))

    def find(self, dst):
        '''
        Returns True if there is an edge towards `dst` in this sequence.
        '''
        if self.head().is_empty():
            return False
        if dst == self.head().dst():
            return True
        return self.tail().find(dst)

    def cardinality(self):
        '''
        Returns the number of edges in this sequence.
        '''
        if self.is_empty():
            return 0
        else:
            return self.tail().cardinality() + 1

    def list(self, src):
        '''
        Returns a list of edges in lexicographical order, e.g., if `src`
        goes to nodes A and B, the returned list would be:
            [ (src, A), (src, B) ]
        '''
        if self.head().is_empty():
            return []
        return [(src, self.head().dst(), self.weight())] + self.tail().list(src)


if __name__ == "__main__":
    log.critical("module contains no main method")
    sys.exit(1)
