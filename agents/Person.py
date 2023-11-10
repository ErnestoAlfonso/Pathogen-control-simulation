from typing import Any
from .FCM_package.FCM_Person import FCM_Person
import random
from random import choice

class person:
    def __init__(self, id):
        self.id = id
        self.state = 0
        self.max_energy = 18
        self.energy = 18
        self.amount_food = 10
        self.count = 0
        self.max_amount_food = 42
        self.money = 10
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
        if self.energy <= 0:
            return 5
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
        self.count += 1
        if self.count % 6 == 0:
            if self.amount_food - 1 >= 0:
                self.amount_food -= 1
        if self.infected == 10:
            bgrpah.graph.delete_node(self.id)
            return 0
        actions = {
            0 : self.go_to_work,
            1 : self.go_to_market,
            2 : self.go_to_hospital,
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
        for i in range(3):
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
                2 * (self.max_amount_food / sens["food_high"][1])
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
                3 * (self.max_energy / sens["energy_high"][1])
            ),
            inv = True
        )

        self.fcm.concepts[sens["energy_low"][0]] = self.fcm.fuzzy(
            self.energy,
            (
                self.max_energy / sens["energy_low"][1],
                3 * (self.max_energy / sens["energy_low"][1])
            )
        )

        # Money
        self.fcm.concepts[sens["money_high"][0]] = self.fcm.fuzzy(
            self.money * (self.amount_food / 3),
            ( 
                market_cost / sens["money_high"][1],
                market_cost * (364 / self.max_amount_food / 3)
            ),
            inv = True
        )

        self.fcm.concepts[sens["money_low"][0]] = self.fcm.fuzzy(
            self.money * (self.amount_food / 3),
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
        self.money += 30
        self.energy -= 1
        for i in range(work.amount_mosq):
            result = random.random() < work.mosquitos[i].prob_of_byte
            if self.infected > 0:
                work.mosquitos[i].infected = True
            
            elif result and work.mosquitos[i].infected:
                self.infected = random.random() * 5
            
            


    def go_to_market(self, bgraph):
        for item in self.freq_places:
            if "Market" in str(item):
                market = item
            else:
                market_places = bgraph.find_place("Market")
                market = choice(market_places)

        list_loc_change = [(self.id, self.place_at_moment, market)]
        bgraph.replace_edges(list_loc_change)

        if self.money - bgraph.graph.market_cost < 0:
            self.amount_food += 10
            self.money -= bgraph.graph.market_cost


        for i in range(market.amount_mosq):
            result = random.random() < market.mosquitos[i].prob_of_byte
            if self.infected > 0:
                market.mosquitos[i].infected = True
            
            elif result and market.mosquitos[i].infected:
                self.infected = random.random() * 5
        
    def go_to_hospital(self, bgraph):
        for item in self.freq_places:
            if "Hospital" in str(item):
                hospital = item
            else:
                hospital_places = bgraph.find_place("Hospital")
                hospital = choice(hospital_places)
        list_loc_change = [(self.id, self.place_at_moment, hospital)]
        bgraph.replace_edges(list_loc_change)
        self.infected -= 1
        for i in range(hospital.amount_mosq):
            result = random.random() < hospital.mosquitos[i].prob_of_byte
            if self.infected > 0:
                hospital.mosquitos[i].infected = True
            
            elif result and hospital.mosquitos[i].infected:
                self.infected = random.random() * 5
    
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
        for i in range(home.amount_mosq):
            result = random.random() < home.mosquitos[i].prob_of_byte
            if self.infected > 0:
                home.mosquitos[i].infected = True
            
            elif result and home.mosquitos[i].infected:
                self.infected = random.random() * 5

        self.energy +=3
    
    def prevent(self, bgraph):
        for item in self.freq_places:
            if "Home" in str(item):
                home = item

        list_loc_change = [(self.id, self.place_at_moment, home)]
        bgraph.replace_edges(list_loc_change)
        result_of_prevent = random.random()
        for i in range(home.amount_mosq):
            if result_of_prevent > 0.5:
                home.mosquitos[i].prob_of_byte -= 0.03

            if result_of_prevent <= 0.5:
                home.mosquitos[i].prob_of_byte -= 0.01

            result = random.random() < home.mosquitos[i].prob_of_byte
            if self.infected > 0:
                home.mosquitos[i].infected = True
            
            elif result and home.mosquitos[i].infected:
                self.infected = random.random() * 5
        






