from numpy import array, zeros 
from scipy.special import expit



class FCM:
    
    def __init__(self, sensitive_concepts : int, internal_concepts : int, action_concepts : int):
        self.nodes_amount = sensitive_concepts + internal_concepts + action_concepts  
        self._sensitive_concepts = sensitive_concepts
        self._internal_concepts = internal_concepts
        self._action_concepts = action_concepts
        self.concepts =  zeros(self.nodes_amount)
        self.causal_graph = zeros((self._sensitive_concepts + self._internal_concepts, self._internal_concepts + self._action_concepts))    
    
    def update_concepts(self):
        old_concepts = self.concepts.copy()
        for i in range(self._sensitive_concepts, self.nodes_amount):
            self.concepts[i] = self.get_newConcept_value(i, old_concepts)

    def get_newConcept_value(self, current_concept : int, old_concepts):
        current = old_concepts[current_concept]
        rows = self.causal_graph.shape[0]
        for i in range(rows):
            current += self.causal_graph[i, current_concept - self._sensitive_concepts] * old_concepts[i]
        result = expit(array([current]))
        return result[0]

    def get_node(self, index : int):
        return self.concepts[index]

    def get_arc_weight(self, x: int, y: int):
        return self.causal_graph[x,y]

    def get_action_concepts(self):
        return self.concepts[self._sensitive_concepts + self._internal_concepts:]
    
    def fuzzy(self, parameter, interval : tuple, inv=False):
        """method for fuzzification 

        Args:
            parameter (float): param to apply fuzzification
            interval (tuple): membership range, like (begin : float, end : float) 
            inv (bool, optional): boolean parameter for apply inverted fuzzy, defaults to False.
        """

        if parameter > interval[1]:
            if inv:
                return 1
            return 0
        if parameter < interval[0]:
            if inv:
                return 0
            return 1
        return (parameter - interval[0])/(interval[1] - interval[0]) if inv else (interval[1] - parameter)/(interval[1] - interval[0])
    

    
            


        