from typing import Generic, TypeVar, Dict, List, Optional
from random import random, randint, choices, sample
from agents.Person import person
from agents.Mosquitos import mosquitos


Node = TypeVar("Node")

class Graphs:
    def __init__(self, amount_nodes, amount_edges, type_Graph):
        self.reset()
        self.amount_nodes = amount_nodes
        self.amount_edges = amount_edges
        self.type_Graph = type_Graph
        self.create_nodes()
        self.create_edges()
    
    def reset(self):
        self.graph = {}
        self.nodes = {}
        self.edges = {}
    
    # region Nodes
    def create_nodes(self):
        i = 0
        

        while i < self.amount_nodes:
            agent_type = {
                "person" : person(i),
                "mosquitos" : mosquitos(i)
            }
            node = agent_type[self.type_Graph]
            self.nodes[i] = node
            self.edges[i] = set()
            i += 1


    def add_node(self, node):
        if node not in self.graph:
            self.nodes[node.id] = node
            self.edges[node.id] = set()
        else:
            raise KeyError("Node is already in the graph")
    
    def delete_node(self, node):
        if node not in self.graph:
            raise KeyError("Node is not in graph")
        else:
            self.delete_edges(node.id)
            self.nodes.pop(node.id)
    
    #endregion
    
    # region Edges
    def create_edges(self):
        nodes_chosens = []
        edge_try = tuple(sample(self.nodes.keys(), k=2))
        for i in range(self.amount_edges):
            while edge_try in nodes_chosens:
                edge_try = tuple(sample(self.nodes.keys(), k=2))
            nodes_chosens.append(edge_try)
        for edge in nodes_chosens:
            self.edges[edge[0]].add(edge[1])
            self.edges[edge[1]].add(edge[0])

    # def add_edges(self, edges: list(tuple)):
    #     for edge in edges:
    #         self.edges[edge[0]].append(edge[1])
    #         self.edges[edge[1]].append(edge[0])
    
    # def delete_edges(self, node):
    #     self.edges.pop(node.id)
    #endregion
    
        


