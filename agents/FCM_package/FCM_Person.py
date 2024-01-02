from .FCM import FCM

class FCM_Person(FCM):
    def __init__(self):
        self._sens_index_params = {
            "people_sick_high" : (0, 1.4),
            "people_sick_low" : (1, 1.4),
            "food_high" : (2, 1.5),
            "food_low" : (3, 1.5),
            "energy_high" : (4, 3),
            "energy_low" : (5, 3),
            "money_high" : (6, 1.5),
            "money_low" : (7, 1.5),
            "sickness_high" : (8, 3.2),
            "sickness_low" : (9, 3.2)
        }
        self._internals_index = {
            "fear" : 10,
            # "loneliness" : 11,
            "hunger" : 11,#12
            "necessity" : 12,
            "disease" : 13,
            "indifference" : 14,
            "tiredness" : 15
            
        }
        self._actions_index = {
            "go_to_work" : 16,
            "go_to_market" : 17,
            "go_to_hospital" : 18,
            "go_around" : 19,
            "study" : 20,
            "rest" : 21,
            "prevent": 22
        } 
        sens = 10
        internal = 6
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
        self.causal_graph[0,0] = 0.6
        self.causal_graph[1,0] = -0.6
        self.causal_graph[8,0] = 1
        self.causal_graph[9,0] = -1
        #hunger
        self.causal_graph[2,1] = 0.4#2
        self.causal_graph[3,1] = -0.4
        #necessity
        self.causal_graph[2,2] = 0.4
        self.causal_graph[3,2] = -0.4
        self.causal_graph[6,2] = 0.6
        self.causal_graph[7,2] = -0.6
        #disease
        self.causal_graph[8,3] = 0.6
        self.causal_graph[9,3] = -0.6
        #indiference
        self.causal_graph[0,4] = -0.16
        self.causal_graph[1,4] = 0.13
        self.causal_graph[4,4] = 0.16
        self.causal_graph[5,4] = -0.16
        self.causal_graph[6,4] = 0.16
        self.causal_graph[7,4] = -0.3
        self.causal_graph[9,4] = 0.16
        #tiredness
        self.causal_graph[4,5] = 1
        self.causal_graph[5,5] = -1

    def _build_internalActions_connections(self):
        #go_to_work
        self.causal_graph[10,6] = -0.16
        # self.causal_graph[11,7] = 1.5
        self.causal_graph[11,6] = 0.3
        self.causal_graph[12,6] = 0.9#1
        self.causal_graph[13,6] = -0.25
        self.causal_graph[15,6] = -0.1
        #go_to_market
        self.causal_graph[10,7] = -0.16
        self.causal_graph[11,7] = 0.6
        self.causal_graph[14,7] = 0.13
        self.causal_graph[15,7] = -0.7#0.1
        #go_to_hospital
        self.causal_graph[15,8] = -1
        self.causal_graph[10,8] = 0.13
        self.causal_graph[13,8] = 1
        #go_around
        self.causal_graph[10,9] = -0.083
        # self.causal_graph[11,10] = 0.6
        self.causal_graph[12,9] = -0.4
        self.causal_graph[14,9] = 0.06
        #study
        self.causal_graph[10,10] = 0.26
        self.causal_graph[12,10] = -0.16
        self.causal_graph[14,10] = 0.05
        #rest
        # self.causal_graph[11,12] = -2
        self.causal_graph[11,11] = -0.2
        self.causal_graph[12,11] = -1
        self.causal_graph[15,11] = 0.8
        #prevent
        self.causal_graph[10,12] = 0.4 #11
        self.causal_graph[12,12] = -0.16
        self.causal_graph[14,12] = 0.11
