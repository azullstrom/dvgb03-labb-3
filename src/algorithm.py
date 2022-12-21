#!/usr/bin/env python3

import sys
import logging

log = logging.getLogger(__name__)

from math import inf

def warshall(adjlist):
    '''
    Returns an NxN matrix that contains the result of running Warshall's
    algorithm.

    Pre: adjlist is not empty.
    '''
    # Fetching Floyd matrix for alteration into Warshall matrix.
    matrix = floyd(adjlist)

    # Swapping inf values with False and integer values with True.
    for i in range(len(matrix)):
        for j in range(len(matrix[i])):
            matrix[i][j] = False if matrix[i][j] == inf else True
    return matrix


def floyd(adjlist):
    '''
    Returns an NxN matrix that contains the result of running Floyd's algorithm.
    Adding 0's in the matrix diagonally if there is no self loop on that position, else
    add the minimum weight to reach that dst from src (direct or indirect).

    Pre: adjlist is not empty.
    '''
    n = adjlist.node_cardinality()
    matrix = [[inf] * n for i in range(n)]
    matrix = adjlist.add_list_to_matrix(matrix)

    for k in range(n):
        for i in range(n):
            for j in range(n):
                matrix[i][j] = 0 if i == j and matrix[i][j] == inf \
                    else min(matrix[i][j], matrix[i][k] + matrix[k][j])
    return matrix


def dijkstra(adjlist, start_node):
    '''
    Returns the result of running Dijkstra's algorithm as two N-length lists:
    1) distance d: here, d[i] contains the minimal cost to go from the node
    named `start_node` to the i:th node in the adjacency list.
    2) edges e: here, e[i] contains the node name that the i:th node's shortest
    path originated from.

    If the index i refers to the start node, set the associated values to None.

    Pre: start_node is a member of adjlist.

    === Example ===
    Suppose that we have the following adjacency matrix:

      a b c
    -+-----
    a|* 1 2
    b|* * 2
    c|* * *

    For start node "a", the expected output would then be:

    d: [ None, 1, 2]
    e: [ None, 'a', 'a' ]

    ####################################
    ##### STUDENT CODE DESCRIPTION #####
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    q: A temporary queue where all nodes are stored. So every node will be checked.
    s: Every completed node is appended in this array.

    Every implemented help functions has their own description for you to read.

    Note: Read info() and set_info() comments in adjlist.py if you need clarity
    in what they're used for in Dijkstra and Prim.
    '''
    n = adjlist.node_cardinality()
    d, e, q, s = [None] * n, [None] * n, [], []
    init_single_source(adjlist, q, start_node)

    while len(q) > 0:
        u = get_min_node(q)
        s.append(u)
        for edge in u.list_edges_object():
            v = adjlist.get_node(edge.dst())
            relax(u, v, edge.weight())
    return get_output(s, d, e)


def prim(adjlist, start_node):
    '''
    Returns the result of running Prim's algorithm as two N-length lists:
    1) lowcost l: here, l[i] contains the weight of the cheapest edge to connect
    the i:th node to the minimal spanning tree that started at `start_node`.
    2) closest c: here, c[i] contains the node name that the i:th node's
    cheapest edge orignated from. 

    If the index i refers to the start node, set the associated values to None.

    Pre: adjlist is setup as an undirected graph and start_node is a member.

    === Example ===
    Suppose that we have the following adjacency matrix:

      a b c
    -+-----
    a|* 1 3
    b|1 * 1
    c|3 1 *

    For start node "a", the expected output would then be:

    l: [ None, 1, 1]
    c: [ None, 'a', 'b' ]

    ####################################
    ##### STUDENT CODE DESCRIPTION #####
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    q: A temporary queue where all nodes are stored. So every node will be checked.
    s: Every completed node is appended in this array.

    Every implemented help functions has their own description for you to read.

    Note: Read info() and set_info() comments in adjlist.py if you need clarity
    in what they're used for in Dijkstra and Prim.
    '''
    n = adjlist.node_cardinality()
    l, c, q, s = [None] * n, [None] * n, [], []
    init_single_source(adjlist, q, start_node)

    while len(q) > 0:
        u = get_min_node(q)
        s.append(u)
        for edge in u.list_edges_object():
            v = adjlist.get_node(edge.dst())
            if v in q and edge.weight() < v.info()[0]:
                v.set_info([edge.weight(), u.name()])
    return get_output(s, l, c)


def init_single_source(adjlist, q, start_node):
    '''
    Initializing the queue with all nodes. Using info, setting start node distance to 0
    with previous node = None and all other unknown nodes to inf with previous node to
    None.
    '''
    q.extend(adjlist.list_nodes_object())
    for node in q:
        if node.name() == start_node:
            node.set_info([0, None])
        else:
            node.set_info([inf, None])


def get_min_node(arr):
    '''
    Returns and pop the dst node with the shortest distance from src.
    '''
    min_index = 0
    for i in range(len(arr)):
        if arr[i].info()[0] < arr[min_index].info()[0]:
            min_index = i
    return arr.pop(min_index)


def relax(u, v, weight):
    '''
    Alters the current node v shortest distance to u.info()[0] + weight if this
    path is quicker than the current distance. Also alters v's previous node.
    '''
    if v.info()[0] > u.info()[0] + weight:
        v.set_info([u.info()[0] + weight, u.name()])


def get_output(nodes, distance, previous):
    '''
    ### HELP FUNCTION ###
    Returns one sorted array "distance" with the shortest path to one node and another
    sorted array "previous" with the previous node in that path.

    Pre: Dijkstra or Prim is called and sends a complete set with nodes
    as first parameter.
    '''
    nodes.sort(key=lambda x: x.name())
    for i, node in enumerate(nodes):
        distance[i] = None if node.info()[0] == 0 else node.info()[0]
        previous[i] = None if node.info()[0] == 0 else node.info()[1]
    return distance, previous


if __name__ == "__main__":
    logging.critical("module contains no main")
    sys.exit(1)
