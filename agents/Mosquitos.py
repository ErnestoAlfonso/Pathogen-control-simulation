

from typing import Any


class mosquitos:
    def __init__(self, id):
        self.id = id
        self.state = 0
        self.hunger = 0
        self.infected = False
        self.prob_of_byte = 0.2
    # def __call__(self, ):
    #     return

    def __repr__(self):
        return "mosquito" + str(self.id)
    
    def locate(self):
        pass