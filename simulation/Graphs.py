from typing import Generic, TypeVar, Dict, List, Optional
from random import random, randint, choices, sample
from agents.Person import person
from places.Locations import Hospital, Home, Market, Work
from tools.graph_tools import find_cliques


Node = TypeVar("Node")

class Graph:
    def __init__(self, amount_nodes, amount_edges):
        self.reset()
        self.amount_nodes = amount_nodes
        self.amount_edges = amount_edges
        self.create_nodes()
        self.create_edges()
        self.bipartite_graph = Bipartite_Graph(self)
    
    def reset(self):
        self.nodes = {}
        self.edges = {}
    
    # region Nodes
    def create_nodes(self):
        i = 0
        while i < self.amount_nodes:
            node = person(i)
            self.nodes[i] = node
            self.edges[i] = set()
            i += 1


    def add_node(self, node):
        if node not in self.nodes:
            self.nodes[node.id] = node
            self.edges[node.id] = set()
        else:
            raise KeyError("Node is already in the graph")
    
    def delete_node(self, node):
        if node not in self.nodes:
            raise KeyError("Node is not in graph")
        else:
            self.delete_edges(node.id)
            self.nodes.pop(node.id)
    
    #endregion
    
    # region Edges
    def create_edges(self):
        nodes_chosens = []
        edge_try = tuple(sample(list(self.nodes.keys()), k=2))
        for i in range(self.amount_edges):
            while edge_try in nodes_chosens:
                edge_try = tuple(sample(list(self.nodes.keys()), k=2))
            nodes_chosens.append(edge_try)
        for edge in nodes_chosens:
            self.edges[edge[0]].add(edge[1])
            self.edges[edge[1]].add(edge[0])

    # def add_edges(self, edges: list(tuple)):
    #     for edge innodes_p
    #         self.edges[edge[0]].append(edge[1])
    #         self.edges[edge[1]].append(edge[0])
    
    # def delete_edges(self, node):
    #     self.edges.pop(node.id)
    #endregion
    
        

class Bipartite_Graph(Graph):
    def __init__(self, graph: Graph):
        self.nodes_L = {}
        self.graph = graph
        self.edges = {}
        self.create_nodes()

        
    def create_nodes(self):
        amount_of_people = len(self.graph.nodes)
        list_cliques = find_cliques(self.graph)
        cliques = set()
        for elto in list_cliques:
            cliques.add(tuple(elto))
        i=0
        for clique in cliques:
            self.nodes_L[i] = Home("Home" + str(i))
            for j in clique:
                self.edges[j] = set()
                self.edges[j].add(self.nodes_L[i])
                self.graph.nodes[j].place_at_moment = self.nodes_L[i]
                self.graph.nodes[j].freq_places.add(self.nodes_L[i])
            i+=1
        # TODO: Find a the best relation between people and places
        node = Hospital("Hospital" + str(i))
        self.nodes_L[i] = node
        i+=1
        node = Work("Work" + str(i))
        self.nodes_L[i] = node
        i+=1
        node = Market("Market" + str(i))
        self.nodes_L[i] = node

# Done
    def replace_edges(self, edges_to_replace: list):
        for item in edges_to_replace:
            self.edges[item[0]].remove(item[1])
            self.edges[item[0]] = set()
            self.edges[item[0]].add(item[2])
        return "edge replaced"
    
    # Find all the type of nodes of one kind. Maked for Hospitals, Works and Markets nodes.
    # Done
    def find_place(self, places):
        places_node = []
        for node in self.nodes_L.values():
            if places in str(node):
                places_node.append(node)
        
        return places_node



