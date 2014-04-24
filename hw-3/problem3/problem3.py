#!/usr/bin/python3
from copy import deepcopy

__author__ = 'jsenko'

# row -> column
graph1 = [[   0, None,    1, None, None],
          [  -2,    0,    4, None,    5],
          [None, None,    0,    0,    2],
          [None,    3, None,    0, None],
          [None, None, None,   -1,    0]
         ]


def reduce(graph, node):
    graph = deepcopy(graph)
    node_count = len(graph)
    for i in range(node_count):
        in_cost = graph[i][node]
        if i != node and in_cost is not None:
            for j in range(node_count):
                out_cost = graph[node][j]
                if j != node and out_cost is not None:
                    cost = in_cost + out_cost
                    if graph[i][j] is None or cost < graph[i][j]:
                        graph[i][j] = cost
                graph[node][j] = None
        graph[i][node] = None
    return graph


def join_out(original_graph, graph, node):
    original_graph = deepcopy(original_graph)
    graph = deepcopy(graph)
    # either join directly or via another node
    # assume that nodes are being added in certain order
    # row
    node_count = len(graph)
    for i in range(node_count):  # for each outgoing edges
        out_cost = original_graph[node][i]
        if i != node and out_cost is not None:
            for j in range(node_count):
                min_cost = graph[i][j]
                if j != node and min_cost is not None:
                    cost = out_cost + min_cost
                    if graph[node][j] is None or cost < graph[node][j]:
                        graph[node][j] = cost
    return graph


def join_in(original_graph, graph, node):
    # either join directly or via another node
    # assume that nodes are being added in certain order
    # row
    original_graph = deepcopy(original_graph)
    graph = deepcopy(graph)
    node_count = len(graph)
    for i in range(node_count):  # for each outgoing edges
        in_cost = original_graph[i][node]
        if i != node and in_cost is not None:
            for j in range(node_count):
                min_cost = graph[j][i]
                if j != node and min_cost is not None:
                    cost = in_cost + min_cost
                    if graph[j][node] is None or cost < graph[j][node]:
                        graph[j][node] = cost
    return graph


def compute(graph, node):
    graph = deepcopy(graph)
    if node == len(graph) - 2:
        return graph
    reduced = reduce(graph, node)
    computed = compute(reduced, node + 1)
    joined = join_out(graph, computed, node)
    joined = join_in(graph, joined, node)
    joined[node][node] = 0  # important!
    return joined


print(compute(graph1, 0))