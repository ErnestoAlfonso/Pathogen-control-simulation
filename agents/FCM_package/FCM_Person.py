from .FCM import FCM

class FCM_Person(FCM):
    def __init__(self):
        self._sens_index_params = {
            "people_sick_high" : (0, 2),
            "people_sick_low" : (1, 2),
            "food_high" : (2, 3),
            "food_low" : (3, 3),
            "energy_high" : (4, 9),
            "energy_low" : (5, 9),
            "money_high" : (6, 1),
            "money_low" : (7, 1),
            "sickness_high" : (8, 3.2),
            "sickness_low" : (9, 3.2)
        }
        self._internals_index = {
            "fear" : 8,
            "loneliness" : 9,
            "hunger" : 10,
            "necessity" : 11,
            "disease" : 12,
            "indifference" : 13,
            "tiredness" : 14
            
        }
        self._actions_index = {
            "go_to_work" : 15,
            "go_to_market" : 16,
            "go_to_hospital" : 17,
            "go_around" : 18,
            "study" : 19,
            "rest" : 20,
            "prevent": 21
        } 
        sens = 10
        internal = 7
        actions = 7
        super().__init__(sens, internal, actions)
        self._build_connections()

    def _build_connections(self):
        """method for assign weight to the arcs of fuzzy map
        """
        self._build_sensInternal_connections()
        self._build_internalActions_connections()
    
    def _build_sensInternal_connections(self):
        #fear
        self.causal_graph[0,0] = 4
        self.causal_graph[1,0] = -4
        self.causal_graph[8,0] = 6
        self.causal_graph[9,0] = -6
        #hunger
        self.causal_graph[2,2] = 4
        self.causal_graph[3,2] = -4
        #necessity
        self.causal_graph[2,3] = 2
        self.causal_graph[3,3] = -2
        self.causal_graph[6,3] = 4
        self.causal_graph[7,3] = -4
        #disease
        self.causal_graph[8,4] = 10
        self.causal_graph[9,4] = -10
        #indiference
        self.causal_graph[1,5] = 1
        self.causal_graph[4,5] = 1
        self.causal_graph[6,5] = 1
        self.causal_graph[9,5] = 1
        #tiredness
        self.causal_graph[4,6] = 4
        self.causal_graph[5,6] = -4

    def _build_internalActions_connections(self):
        #go_to_work
        self.causal_graph[10,7] = -1
        self.causal_graph[11,7] = 1
        self.causal_graph[13,7] = 4
        self.causal_graph[14,7] = -2.5
        #go_to_market
        self.causal_graph[10,8] = -0.8
        self.causal_graph[12,8] = 4
        self.causal_graph[15,8] = 0.8
        self.causal_graph[16,8] = -1
        #go_to_hospital
        self.causal_graph[10,9] = 0.8
        self.causal_graph[14,9] = 6
        #go_around
        self.causal_graph[10,10] = -2.5
        self.causal_graph[11,10] = 1.5
        self.causal_graph[15,10] = 1
        #study
        self.causal_graph[10,11] = 1.6
        self.causal_graph[15,11] = 2
        #rest
        self.causal_graph[15,12] = 1
        self.causal_graph[16,12] = 4
        #prevent
        self.causal_graph[10,13] = 3.5
        self.causal_graph[15,13] = 1.3
