from typing import Generic, TypeVar, Dict, List, Optional
from random import random, randint, choices, sample
from agents.Person import person
from agents.Mosquitos import mosquitos
from places.Locations import Hospital, Home, Market, Work
from tools.graph_m_tools import find_cliques
import igraph as ig


Node = TypeVar("Node")

class Graph_m():
    def __init__(self, amount_nodes, prob_of_edges, market_cost, amount_mosq_per_places, prob_mosq_bite_ap, prob_inf_if_mosq_bite):
        self.reset()
        self.amount_nodes = amount_nodes
        self.prob_of_edges = prob_of_edges
        self.market_cost = market_cost
        self.prob_mosq_bite_ap = prob_mosq_bite_ap
        self.prob_inf_if_mosq_bite = prob_inf_if_mosq_bite
        self.amount_mosq_per_places = amount_mosq_per_places
        self.graph = ig.Graph.GRG(self.amount_nodes, prob_of_edges)
        
        self.add_prop_person()
        self.create_nodes()
        self.create_edges()
        self.bipartite_graph = Bipartite_Graph(self)
    
    def reset(self):
        self.nodes = {}
        self.edges = {}
        self.graph = None

    def add_prop_person(self):
        my_list = []
        i=0
        while i < self.amount_nodes:
            node = person(i)
            my_list.append(node)
            i+=1
        self.graph.vs["person"] = my_list
        print(self.graph.vs["person"])

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
            self.delete_edges(node)
            self.nodes.pop(node)
    
    #endregion
    
    # region Edges
    def create_edges(self):
        nodes = []
        for node in self.graph.vs:
            nodes = self.graph.neighbors(node)
        # edge_try = tuple(sample(list(self.nodes.keys()), k=2))
        # for i in range(self.amount_edges):
        #     while edge_try in nodes_chosens:
        #         edge_try = tuple(sample(list(self.nodes.keys()), k=2))
        #     nodes_chosens.append(edge_try)
            for n in nodes:
                self.edges[node.index].add(n)
                self.edges[n].add(node.index)

    # def add_edges(self, edges: list(tuple)):
    #     for edge innodes_p
    #         self.edges[edge[0]].append(edge[1])
    #         self.edges[edge[1]].append(edge[0])
    
    def delete_edges(self, node):
        self.edges.pop(node)
    #endregion


    # region Params
    def amount_people_sick(self):
        count = 0
        for item in self.nodes.values():
            if item.infected == 1:
                count += 1
        
        return count
    # endregion



class Bipartite_Graph(Graph_m):
    def __init__(self, graph: Graph_m):
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
            self.nodes_L[i] = Home("Home" + str(i), self.graph.amount_mosq_per_places)
            for item in range(self.nodes_L[i].amount_mosq):
                mos = mosquitos(item, self.graph.prob_mosq_bite_ap)
                self.nodes_L[i].mosquitos.append(mos)
            for j in clique:
                if len(self.graph.graph.vs["person"][j].freq_places) == 0:
                    self.edges[j] = set()
                    self.edges[j].add(self.nodes_L[i])
                    self.graph.nodes[j].place_at_moment = self.nodes_L[i]
                    self.graph.nodes[j].freq_places.add(self.nodes_L[i])
                    self.graph.graph.vs["person"][j].place_at_moment = self.nodes_L[i]
                    self.graph.graph.vs["person"][j].freq_places.add(self.nodes_L[i])
                    # TODO: Delete self.graph.nodes and only use .vs["person"]
            i+=1
        # TODO: Find a the best relation between people and places
        node = Hospital("Hospital" + str(i), self.graph.amount_mosq_per_places)
        self.nodes_L[i] = node
        for item in range(self.nodes_L[i].amount_mosq):
            mos = mosquitos(item, self.graph.prob_mosq_bite_ap)
            self.nodes_L[i].mosquitos.append(mos)
            
        i += 1
        node = Work("Work" + str(i), self.graph.amount_mosq_per_places)
        self.nodes_L[i] = node
        for item in range(self.nodes_L[i].amount_mosq):
            mos = mosquitos(item, self.graph.prob_mosq_bite_ap)
            self.nodes_L[i].mosquitos.append(mos)
            self.nodes_L[i].mosquitos[item].infected = True
        i += 1
        node = Market("Market" + str(i), self.graph.amount_mosq_per_places)
        self.nodes_L[i] = node
        for item in range(self.nodes_L[i].amount_mosq):
            mos = mosquitos(item, self.graph.prob_mosq_bite_ap)
            self.nodes_L[i].mosquitos.append(mos)

# Done
    def replace_edges(self, edges_to_replace: list):
        for item in edges_to_replace:
            self.edges[item[0]].discard(item[1])
            self.edges[item[0]] = set()
            self.edges[item[0]].add(item[2])
            self.graph.graph.vs["person"][item[0]].place_at_moment = list(self.edges[item[0]])[0]
        return "edge replaced"
    
    # Find all the type of nodes of one kind. Maked for Hospitals, Works and Markets nodes.
    # Done
    def find_place(self, places):
        places_node = []
        for node in self.nodes_L.values():
            if places in str(node):
                places_node.append(node)
        
        return places_node



