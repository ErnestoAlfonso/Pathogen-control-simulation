from typing import Any
from .FCM_package.FCM_Person import FCM_Person
from ..simulation.Graphs import Graph, Bipartite_Graph
from random import choice

# "go_to_work" : 15,
#             "go_to_market" : 16,
#             "go_to_hospital" : 17,
#             "go_around" : 18,
#             "study" : 19,
#             "rest" : 20,
#             "prevent": 21
class person:
    def __init__(self, id):
        self.id = id
        self.state = 0
        self.energy = 16
        self.money = 0
        self.infected = False
        self.place_at_moment = 0
        self.freq_places = set()
        self.fcm = FCM_Person()
        
    # def __call__(self, id):
    #     p = person(id)
    #     return p

    def __repr__(self):
        return "person" + self.id

    def locate(self):
        pass

    
    def get_perception(self, graph):
        pass

    def go_to_work(self, bgraph: Bipartite_Graph):
        for item in self.freq_places:
            if "Work" in item:
                work = item
            else: 
                work_places = bgraph.find_place("Work")
                work = choice(work_places)
        list_loc_change = [(self.id, self.place_at_moment, work)]
        bgraph.replace_edges(list_loc_change)


    def go_to_market(self, bgraph: Bipartite_Graph):
        for item in self.freq_places:
            if "Market" in item:
                market = item
            else:
                market_places = bgraph.find_place("Market")
                market = choice(market_places)
        
        list_loc_change = [(self.id, self.place_at_moment, market)]
        bgraph.replace_edges(list_loc_change)
        
    def go_to_hospital(self, bgraph: Bipartite_Graph):
        for item in self.freq_places:
            if "Hospital" in item:
                hospital = item
            else:
                hospital_places = bgraph.find_place("Hospital")
                hospital = choice(hospital_places)
        list_loc_change = [(self.id, self.place_at_moment,hospital)]
        bgraph.replace_edges(list_loc_change)
    
    def study(self, bgraph: Bipartite_Graph):
        pass

    def rest(self, bgraph: Bipartite_Graph):
        for item in self.freq_places:
            if "Home" in item:
                home = item
        
        list_loc_change = [(self.id, self.place_at_moment, home)]
        bgraph.replace_edges(list_loc_change)

        self.energy = 16
    
    def prevent(self, bgraph: Bipartite_Graph):
        for item in self.freq_places:
            if "Home" in item:
                home = item
        
        list_loc_change = [(self.id, self.place_at_moment, home)]
        bgraph.replace_edges(list_loc_change)

        # TODO: make a parameter in mosquitos to change here to prevent bites




