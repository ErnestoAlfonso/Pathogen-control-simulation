from .FCM import FCM

class FCM_Predator(FCM):
    def __init__(self):
        self._sens_index_params = {
            "prey_close" : (0, 1.6),
            "prey_far" : (1, 1.6),
            "food_close" : (2, 2),
            "food_far" : (3, 2),
            "energy_low" : (4, 1.5),
            "energy_high" : (5, 1.5),
            "food_local_high" : (6, 5),
            "food_local_low" : (7, 5)
        }
        self._internals_index = {
            "chase_away" : 8,
            "hunger" : 9,
            "satisfaction" : 10,
            "nuisance" : 11
        }
        self._actions_index = {
            "hunt" : 12,
            "search_food" : 13,
            "exploration" : 14,
            "wait" : 15,
            "eat" : 16
        }
        sens = 8
        internal = 4
        actions = 5
        super().__init__(sens, internal, actions)
        self._build_connections()

    def _build_connections(self):
        """method for assign weight to the arcs of fuzzy map
        """
        self._build_sensInternal_connections()
        self._build_internalActions_connections()

    def _build_sensInternal_connections(self):
        #chase_away
        self.causal_graph[0,0] = 2
        self.causal_graph[1,0] = -0.5
        self.causal_graph[2,0] = 0.2
        self.causal_graph[3,0] = 0.3
        self.causal_graph[4,0] = 4
        self.causal_graph[5,0] = -3.5
        self.causal_graph[6,0] = 2
        self.causal_graph[7,0] = 1.7

        #hunger
        self.causal_graph[0,1] = 0.2
        self.causal_graph[1,1] = -0.7
        self.causal_graph[2,1] = 0.7
        self.causal_graph[4,1] = 3.2
        self.causal_graph[5,1] = -4
        self.causal_graph[6,1] = 0.5
        #satisfaction
        self.causal_graph[0,2] = 0.5
        self.causal_graph[1,2] = -0.5
        self.causal_graph[2,2] = 0.5
        self.causal_graph[3,2] = -0.7
        self.causal_graph[4,2] = -1.5
        self.causal_graph[5,2] = 2
        self.causal_graph[6,2] = 1.5
        self.causal_graph[7,2] = -1.5
        #nuisance
        self.causal_graph[0,3] = -0.5
        self.causal_graph[1,3] = 0.5
        self.causal_graph[2,3] = -0.5
        self.causal_graph[3,3] = 0.7
        self.causal_graph[4,3] = 1.5
        self.causal_graph[5,3] = -2
        self.causal_graph[6,3] = -1.5
        self.causal_graph[7,3] = 1.5

    def _build_internalActions_connections(self):
        #hunt
        self.causal_graph[8,4] = 2.5
        self.causal_graph[9,4] = 1
        self.causal_graph[10,4] = -0.3
        self.causal_graph[11,4] = -1.2
        #search_food
        self.causal_graph[8,5] = -0.5
        self.causal_graph[9,5] = 0.4
        self.causal_graph[10,5] = -0.4
        self.causal_graph[11,5] = 0.5
        #exploration
        self.causal_graph[8,6] = -0.1
        self.causal_graph[9,6] = -0.1
        self.causal_graph[10,6] = -2
        self.causal_graph[11,6] = 0.4
        #wait
        self.causal_graph[8,7] = -0.4
        self.causal_graph[9,7] = -0.4
        self.causal_graph[10,7] = 0.5
        self.causal_graph[11,7] = -1
        #eat
        self.causal_graph[8,8] = -2
        self.causal_graph[9,8] = 2.5
        self.causal_graph[10,8] = -0.9
        self.causal_graph[11,8] = -0.3