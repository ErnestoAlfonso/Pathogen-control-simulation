


class Place:
    def __init__(self, nombre):
        self.nombre = nombre
        self.amount_mosq = 10
        self.mosquitos = []
    
    def type(self):
        return "place"
    
    def __str__(self):
        return self.nombre + "-" + str(self.amount_mosq)

    def __repr__(self):
        return self.nombre + "-" + str(self.amount_mosq)


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
