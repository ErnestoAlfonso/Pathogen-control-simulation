from .FCM import FCM

class FCM_Person(FCM):
    def __init__(self):
        self._sens_index_params = {
            "people_sick_high" : (0, 2),
            "people_sick_low" : (1, 2),
            "food_high" : (2, 3),
            "food_low" : (3, 3),
            "energy_low" : (4, 1.5),
            "energy_high" : (5, 1.5),
            "money_high" : (6, 5),
            "money_low" : (7, 5),
            "sickness_high" : (8,4),
            "sickness_low" : (9,4)
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
    
    # TODO: implement this with the params in the init
    def _build_sensInternal_connections(self):
        #fear
        self.causal_graph[0,0] = 4
        self.causal_graph[1,0] = -4
        self.causal_graph[4,0] = 0.4
        #hunger
        self.causal_graph[2,1] = 0.5
        self.causal_graph[4,1] = 4
        self.causal_graph[5,1] = -4
        self.causal_graph[6,1] = 0.2
        self.causal_graph[7,1] = -0.2
        #satisfaction
        self.causal_graph[0,2] = -1
        self.causal_graph[1,2] = 0.5
        self.causal_graph[2,2] = 0.5
        self.causal_graph[3,2] = -0.7
        self.causal_graph[4,2] = -2.2
        self.causal_graph[5,2] = 1.5
        self.causal_graph[6,2] = 1.1
        self.causal_graph[7,2] = -1.1
        #nuisance
        self.causal_graph[0,3] = 1
        self.causal_graph[1,3] = -0.5
        self.causal_graph[2,3] = -0.5
        self.causal_graph[3,3] = 0.7
        self.causal_graph[4,3] = 2.2
        self.causal_graph[5,3] = -1.5
        self.causal_graph[6,3] = -1.1
        self.causal_graph[7,3] = 1.1

    def _build_internalActions_connections(self):
        #escape
        self.causal_graph[8,4] = 3.5
        self.causal_graph[9,4] = -0.8
        self.causal_graph[10,4] = -0.1
        self.causal_graph[11,4] = 0.4
        #search_food
        self.causal_graph[8,5] = -0.8
        self.causal_graph[9,5] = 2.1
        self.causal_graph[10,5] = -0.8
        self.causal_graph[11,5] = 1
        #exploration
        self.causal_graph[8,6] = 0.3
        self.causal_graph[9,6] = 0.7
        self.causal_graph[10,6] = -2
        self.causal_graph[11,6] = 2
        #wait
        self.causal_graph[8,7] = -1
        self.causal_graph[9,7] = -0.5
        self.causal_graph[10,7] = 0.5
        self.causal_graph[11,7] = -1.2
        #eat
        self.causal_graph[6,8] = 2.6
        self.causal_graph[7,8] = -4
        self.causal_graph[8,8] = -1
        self.causal_graph[9,8] = 3.5
        self.causal_graph[10,8] = -0.1
        self.causal_graph[11,8] = -0.7
