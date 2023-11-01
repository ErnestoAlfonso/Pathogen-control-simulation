from multiprocessing import Process
import datetime
from graph_world.Graphs_m import Graph_m, Bipartite_Graph
import time

def run_simulation(amount_nodes, amount_edges, market_cost):
        # Definir la duración de la simulación
    duracion_simulacion = datetime.timedelta(hours = 5)

    hora_inicial = datetime.datetime(2023, 10, 22, 10, 0)

    # Definir el paso de tiempo
    paso_de_tiempo = datetime.timedelta(hours = 1)

    # Definir la hora de inicio de la simulación
    hora_actual = datetime.datetime(2023, 10, 22, 10, 0)  # Por ejemplo, 21 de septiembre de 2023 a las 9:00 a.m.

    graph = Graph_m(amount_nodes,amount_edges, market_cost)
    dictOfAction = {}
    
    
    
    for key in graph.graph.vs["person"]:
        dictOfAction[key.id] = []
    # Realizar la simulación
    # TODO: Use parallelism to make this more efficient.
    processes = []
    start = time.time()
    while hora_actual <= hora_inicial + duracion_simulacion:
    # for i in range(3):
    #     processes.append(Process(target = action_for_person,args=(graph,hora_actual, hora_inicial, duracion_simulacion, paso_de_tiempo,i)))
    #     processes[i].start()
    #     print("Proceso %d lanzado." % (i + 1))

    
    # for process in processes:
    #     process.join()
        for person in graph.graph.vs["person"]:
            person.get_perception(graph)
            action = person.choose_action()
            person.energy -= 1
            person.make_action(action, graph.bipartite_graph)
            id = str(person)
            dictOfAction[int(id[len(id)-1])].append(DFActions(action, person))
        # Actualizar la hora actual
        hora_actual += paso_de_tiempo
    end = time.time()
    print(f"La persona 0 hizo lo siguiente...{dictOfAction[1]}")
    print(f"Tiempo sin paralelismo {end - start}")
    print("La ejecución a concluído.")
    # simulat = "Termino la simulacion"
    # return simulat


def DFActions(action, person):
    if action == 0:
        return "ESTOY CAMINO AL HOSPITAL " + str(person)
    elif action == 1:
        return "ESTOY CAMINO AL MERCADO " + str(person)
    elif action == 2:
        return "ESTOY CAMINO AL TRABAJO " + str(person) 
    elif action == 3:
        return "ESTOY CAMINANDO ALREDEDOR " + str(person) 
    elif action == 4:
        return "ESTOY ESTUDIANDO " + str(person)
    elif action == 5:
        return "ESTOY DESCANSANDO " + str(person)
    elif action == 6:
        return "ESTOY PREVINIENDO " + str(person)

def action_for_person(graph: Graph_m, hora_actual, hora_inicial, duracion_simulacion, paso_de_tiempo, k):
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
                dictOfAction[int(id[len(id)-1])].append(DFActions(action, person))
        
        hora_actual += paso_de_tiempo
    return f"Termino el proceso {k}"