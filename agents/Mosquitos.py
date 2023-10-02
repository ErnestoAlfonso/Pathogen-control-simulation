

from typing import Any


class mosquitos:
    def __init__(self, id):
        self.id = id
        self.state = 0
        self.infected = False
        self.prob_of_byte = 0
    # def __call__(self, ):
    #     return

    def __repr__(self):
        return "mosquito" + self.id
    
    def locate(self):
        pass