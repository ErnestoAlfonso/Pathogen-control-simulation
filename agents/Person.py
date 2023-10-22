from typing import Any
from .FCM_package.FCM_Person import FCM_Person
import random
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
        self.max_energy = 18
        self.energy = 18
        self.amount_food = 10
        self.max_amount_food = 42
        self.money = 0
        self.infected = 0
        self.max_infection = 10
        self.place_at_moment = 0
        self.freq_places = set()
        self.fcm = FCM_Person()
        
    # def __call__(self, id):
    #     p = person(id)
    #     return p

    def __repr__(self):
        return "person" + str(self.id)

    def locate(self):
        pass

    def choose_action(self):
        actions = list(self.fcm.get_action_concepts())
        sum_actions = sum(actions)
        for i in range(len(actions)):
            actions[i] = actions[i] / sum_actions
        r = random.random()
        inf = 0
        sup = 1
        for i in range(len(actions)):
            if actions[i] > inf and actions[i] < r:
                inf = actions[i]
            if actions[i] < sup and actions[i] > r:
                sup = actions[i]
        if sup == 1:
            return actions.index(inf)
        if inf == 0:
            return 0
        
        return actions.index(sup)
    
    def make_action(self, action, bgrpah):
        actions = {
            0 : self.go_to_hospital,
            1 : self.go_to_market,
            2 : self.go_to_work,
            3 : self.go_around,
            4 : self.study,
            5 : self.rest,
            6 : self.prevent
        }

        return actions[action](bgrpah)

    
    def get_perception(self, graph):
        people_sick = graph.amount_people_sick()
        amount_people = graph.amount_nodes
        self.update_sensitives_concept(people_sick, amount_people, graph.market_cost)

        self.fcm.update_concepts()

    def update_sensitives_concept(self, amount_people_sick, amount_people, market_cost):
        sens = self.fcm._sens_index_params

        # Sick_person
        self.fcm.concepts[sens["people_sick_high"][0]] = self.fcm.fuzzy(
            amount_people_sick,
            (
                amount_people / sens["people_sick_high"][1],
                2 * (amount_people / sens["people_sick_high"][1])
            ),
            inv = True
        )

        self.fcm.concepts[sens["people_sick_low"][0]] = self.fcm.fuzzy(
            amount_people_sick,
            (
                amount_people / sens["people_sick_low"][1],
                2 * (amount_people / sens["people_sick_low"][1])
            )
        )

        # Food
        self.fcm.concepts[sens["food_high"][0]] = self.fcm.fuzzy(
            self.amount_food,
            (
                self.max_amount_food / sens["food_high"][1],
                2 * (self.amount_food / sens["food_high"][1])
            ),
            inv = True
        )

        self.fcm.concepts[sens["food_low"][0]] = self.fcm.fuzzy(
            self.amount_food,
            (
                self.max_amount_food / sens["food_low"][1],
                2 * (self.max_amount_food / sens["food_low"][1])
            )
        )


        # Energy
        self.fcm.concepts[sens["energy_high"][0]] = self.fcm.fuzzy(
            self.energy,
            (
                self.max_energy / sens["energy_high"][1],
                2 * (self.max_energy / sens["energy_high"][1])
            ),
            inv = True
        )

        self.fcm.concepts[sens["energy_low"][0]] = self.fcm.fuzzy(
            self.energy,
            (
                self.max_energy / sens["energy_low"][1],
                2 * (self.max_energy / sens["energy_low"][1])
            )
        )

        # Money
        self.fcm.concepts[sens["money_high"][0]] = self.fcm.fuzzy(
            self.money + 210 * (self.amount_food / 3),
            ( 
                market_cost / sens["money_high"][1],
                market_cost * (364 / self.max_amount_food / 3)
            ),
            inv = True
        )

        self.fcm.concepts[sens["money_low"][0]] = self.fcm.fuzzy(
            self.money + 210 * (self.amount_food / 3),
            ( 
                market_cost / sens["money_low"][1],
                market_cost * (364 / self.max_amount_food / 3)
            )
        )


        # Sick
        self.fcm.concepts[sens["sickness_high"][0]] = self.fcm.fuzzy(
            self.infected,
            (
                self.max_infection / sens["sickness_high"][1],
                3 * (self.max_infection / sens["sickness_high"][1])
            ),
            inv = True
        )

        self.fcm.concepts[sens["sickness_low"][0]] = self.fcm.fuzzy(
            self.infected,
            (
                self.max_infection / sens["sickness_low"][1],
                2 * (self.max_infection / sens["sickness_low"][1])
            )
        )



    def go_to_work(self, bgraph):
        for item in self.freq_places:
            if "Work" in str(item):
                work = item
            else: 
                work_places = bgraph.find_place("Work")
                work = choice(work_places)
        list_loc_change = [(self.id, self.place_at_moment, work)]
        bgraph.replace_edges(list_loc_change)


    def go_to_market(self, bgraph):
        for item in self.freq_places:
            if "Market" in str(item):
                market = item
            else:
                market_places = bgraph.find_place("Market")
                market = choice(market_places)
        
        list_loc_change = [(self.id, self.place_at_moment, market)]
        bgraph.replace_edges(list_loc_change)
        
    def go_to_hospital(self, bgraph):
        for item in self.freq_places:
            if "Hospital" in str(item):
                hospital = item
            else:
                hospital_places = bgraph.find_place("Hospital")
                hospital = choice(hospital_places)
        list_loc_change = [(self.id, self.place_at_moment,hospital)]
        bgraph.replace_edges(list_loc_change)
    
    def study(self, bgraph):
        pass

    def go_around(self, bgraph):
        pass

    def rest(self, bgraph):
        for item in self.freq_places:
            if "Home" in str(item):
                home = item
        
        list_loc_change = [(self.id, self.place_at_moment, home)]
        bgraph.replace_edges(list_loc_change)

        self.energy = 16
    
    def prevent(self, bgraph):
        for item in self.freq_places:
            if "Home" in str(item):
                home = item
        
        list_loc_change = [(self.id, self.place_at_moment, home)]
        bgraph.replace_edges(list_loc_change)

        # TODO: make a parameter in mosquitos to change here to prevent bites
    
    




