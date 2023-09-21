


class Place:
    def __init__(self, nombre):
        self.nombre = nombre
        self.amount_mosq = 0
    
    def type(self):
        return "place"


class Home(Place):
    def type(self):
        return "home"


class Work(Place):
    def type(self):
        return "work"


class Hospital(Place):
    def type(self):
        return "hospital"


class Market(Place):
    def type(self):
        return "market"
