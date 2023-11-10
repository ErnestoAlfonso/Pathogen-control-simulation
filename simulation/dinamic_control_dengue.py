from multiprocessing import Process
import datetime
from graph_world.Graphs_m import Graph_m, Bipartite_Graph
import time

class Simulation:
    def __init__(self, amount_nodes, dur_hour, market_cost, prob_of_edges, amount_mosq_per_place):
        self.amount_nodes = amount_nodes
        self.dur_hour = dur_hour
        self.market_cost = market_cost
        self.prob_of_edges = prob_of_edges
        self.amount_mosq_per_place = amount_mosq_per_place


    def run_simulation(self):
            # Definir la duración de la simulación
        duracion_simulacion = datetime.timedelta(hours = self.dur_hour)

        hora_inicial = datetime.datetime(2023, 10, 22, 7, 0)

        # Definir el paso de tiempo
        paso_de_tiempo = datetime.timedelta(hours = 1)

        # Definir la hora de inicio de la simulación
        hora_actual = datetime.datetime(2023, 10, 22, 8, 0)  # Por ejemplo, 22 de septiembre de 2023 a las 8:00 a.m.

        graph = Graph_m(self.amount_nodes,self.prob_of_edges, self.market_cost, self.amount_mosq_per_place)
        dictOfAction = {}
        self.dictOfHours = {}
        pers = []
        dead_person = []
        
        for key in graph.graph.vs["person"]:
            dictOfAction[key.id] = []
        for hour in range(self.dur_hour):
            self.dictOfHours[hour] = []
        # Realizar la simulación
        # TODO: Use parallelism to make this more efficient.
        processes = []
        start = time.time()
        count = -1
        while hora_actual <= hora_inicial + duracion_simulacion:
            count += 1
        # for i in range(3):
        #     processes.append(Process(target = action_for_person,args=(graph,hora_actual, hora_inicial, duracion_simulacion, paso_de_tiempo,i)))
        #     processes[i].start()
        #     print("Proceso %d lanzado." % (i + 1))

        
        # for process in processes:
        #     process.join()
            for person in graph.graph.vs["person"]:
                try:
                    graph.nodes[person.id]
                except:
                    continue
                person.get_perception(graph)
                action = person.choose_action()
                person.make_action(action, graph.bipartite_graph)
                person.energy -= 1
                try:
                    node = graph.nodes[person.id]
                except:
                    dead_person.append(person.id)
                dictOfAction[person.id].append(self.DFActions(action, person))
                self.dictOfHours[count].append((person.id, True if person.infected > 0 else False))
            # Actualizar la hora actual

            hora_actual += paso_de_tiempo

            if hora_actual.hour == 0 and hora_actual.minute == 0:
                for person in graph.graph.vs["person"]:
                    if person.infected > 0:
                        person.infected += 0.5
                    if person.infected > 10:
                        person.infected = 10

        for person in graph.graph.vs["person"]:
            if person.infected > 0:
                pers.append(person)
        end = time.time()
        print(f"Hechos que hizo una persona...{dictOfAction[3]}")
        print(f"Tiempo sin paralelismo {end - start}")
        print("La ejecución a concluído.")
        print("Personas infectadas")
        print(pers)
        print("Personas muertas")
        print(dead_person)
        # simulat = "Termino la simulacion"
        return graph.graph


    def DFActions(self, action, person):
        if action == 0:
            return "ESTOY CAMINO AL TRABAJO " + str(person)
        elif action == 1:
            return "ESTOY CAMINO AL MERCADO " + str(person)
        elif action == 2:
            return "ESTOY CAMINO AL HOSPITAL " + str(person) 
        elif action == 3:
            return "ESTOY CAMINANDO ALREDEDOR " + str(person) 
        elif action == 4:
            return "ESTOY ESTUDIANDO " + str(person)
        elif action == 5:
            return "ESTOY DESCANSANDO " + str(person)
        elif action == 6:
            return "ESTOY PREVINIENDO " + str(person)

    def action_for_person(self,graph: Graph_m, hora_actual, hora_inicial, duracion_simulacion, paso_de_tiempo, k):
        dictOfAction = {}
        for key in graph.nodes:
            dictOfAction[key] = []
        while hora_actual <= hora_inicial + duracion_simulacion:
            for person in graph.nodes.values():
                    person.get_perception(graph)
                    action = person.choose_action()
                    person.energy -= 1
                    person.make_action(action, graph.bipartite_graph)
                    id = str(person)
                    dictOfAction[int(id[len(id)-1])].append(self.DFActions(action, person))
            
            hora_actual += paso_de_tiempo
        return f"Termino el proceso {k}"