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
        self.causal_graph[2,1] = 2.5#2
        self.causal_graph[3,1] = -2.5
        #necessity
        self.causal_graph[2,2] = 2.5
        self.causal_graph[3,2] = -2.5
        self.causal_graph[6,2] = 4
        self.causal_graph[7,2] = -4
        #disease
        self.causal_graph[8,3] = 4
        self.causal_graph[9,3] = -4
        #indiference
        self.causal_graph[0,4] = -1
        self.causal_graph[1,4] = 0.8
        self.causal_graph[4,4] = 1
        self.causal_graph[5,4] = -1
        self.causal_graph[6,4] = 1
        self.causal_graph[7,4] = -2
        self.causal_graph[9,4] = 1
        #tiredness
        self.causal_graph[4,5] = 4
        self.causal_graph[5,5] = -4

    def _build_internalActions_connections(self):
        #go_to_work
        self.causal_graph[10,6] = -1
        # self.causal_graph[11,7] = 1.5
        self.causal_graph[11,6] = 2
        self.causal_graph[12,6] = 4
        self.causal_graph[13,6] = -1.5
        self.causal_graph[15,6] = -0.8
        #go_to_market
        self.causal_graph[10,7] = -1
        self.causal_graph[11,7] = 4
        self.causal_graph[14,7] = 0.8
        self.causal_graph[15,7] = -1
        #go_to_hospital
        self.causal_graph[10,8] = 0.8
        self.causal_graph[13,8] = 6
        #go_around
        self.causal_graph[10,9] = -0.5
        # self.causal_graph[11,10] = 0.6
        self.causal_graph[12,9] = -2.5
        self.causal_graph[14,9] = 0.4
        #study
        self.causal_graph[10,10] = 1.6
        self.causal_graph[12,10] = -1
        self.causal_graph[14,10] = 0.3
        #rest
        # self.causal_graph[11,12] = -2
        self.causal_graph[15,11] = 1.5
        #prevent
        self.causal_graph[10,12] = 2.5 #11
        self.causal_graph[12,12] = -1
        self.causal_graph[14,12] = 0.7
