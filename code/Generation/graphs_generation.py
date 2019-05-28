from random import choice, randint
from typing import List, Union, Tuple
from itertools import combinations

import networkx as nx

from Simulation.SimulationGraph import SimulationGraph


def connected_gnp_graph(n: int, completion: float = 0.5) -> SimulationGraph:
    """
    Generates a random simulation graph with n nodes, where every edge from complete graph is added with givem probability
    :param n: number of nodes
    :param completion: edge creation probability
    :return: generated SimulationGraph
    """
    G = nx.fast_gnp_random_graph(n, completion)
    components = [list(component) for component in nx.connected_components(G)]

    for comp_a, comp_b in zip(components[1:], components[:-1]):
        e = (choice(comp_a), choice(comp_b))
        G.add_edge(*e)

    return SimulationGraph(G)


def barabasi_albert_graph(n: int, m: int) -> SimulationGraph:
    """
    Generates a random simulation graph according to the Barabási–Albert preferential attachment model
    :param n: number of nodes
    :param m: number of edges to attach from new node to existing node
    :return: Generated SimulationGraph
    """
    return SimulationGraph(nx.barabasi_albert_graph(n, m))


def add_groups_connections(G: nx.Graph, groups: List[List[int]], max_connections: int) -> nx.Graph:
    """
    Adds random number of connections between nodes from every pair of groups
    :param G: input graph
    :param groups: List of lists of nodes in groups
    :return: result graph
    """
    for group_a, group_b in combinations(groups, 2):
        connections = randint(1, max_connections)
        for i in range(connections):
            u = choice(group_a)
            v = choice(group_b)
            G.add_edge(u, v)
    return G


def groups_graph(groups_sizes: List[int], groups_completion: Union[List[float], float],
                 max_connections: int) -> Tuple[SimulationGraph, List[List[int]]]:
    """
    Generates graph with many connections inside groups and few connections between groups.
    Every group is generated by connected_gnp_graph function. Between every pair of groups will be
    generated random number of edges (from 1 to max_connections)
    :param groups_sizes: List of groups sizes
    :param groups_completion: List of values of completion of every group
        or single value if all groups have same completion
    :param max_connections: number of max connections between pairs of groups
    :return: Tuple: generated graph, list of groups
    """

    if not isinstance(groups_completion, list):
        groups_completion = [groups_completion] * len(groups_sizes)

    if len(groups_sizes) != len(groups_completion):
        raise ValueError(f"Length of groups_sizes ({len(groups_sizes)}) and "
                         f"groups_completion ({len(groups_completion)}) must be same ")

    G = nx.Graph()
    groups = list()
    added_nodes = 0

    for size, completion in zip(groups_sizes, groups_completion):
        G_a = connected_gnp_graph(size, completion)
        G = nx.disjoint_union(G, G_a)
        groups.append(list(range(added_nodes, added_nodes + size)))
        added_nodes += size

    G = add_groups_connections(G, groups, max_connections=max_connections)

    return SimulationGraph(G), groups