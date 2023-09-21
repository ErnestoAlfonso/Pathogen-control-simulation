

from typing import Any


class person:
    def __init__(self, id):
        self.id = id
        self.state = 0
        self.infected = False
        
    # def __call__(self, id):
    #     p = person(id)
    #     return p

    def locate(self):
        pass