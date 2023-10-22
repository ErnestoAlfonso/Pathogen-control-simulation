import datetime
from graph_world.Graphs import Graph, Bipartite_Graph

def run_simulation(amount_nodes, amount_edges, market_cost):
        # Definir la duración de la simulación
    duracion_simulacion = datetime.timedelta(hours=5)

    hora_inicial = datetime.datetime(2023, 10, 22, 10, 0)

    # Definir el paso de tiempo
    paso_de_tiempo = datetime.timedelta(hours=1)

    # Definir la hora de inicio de la simulación
    hora_actual = datetime.datetime(2023, 10, 22, 10, 0)  # Por ejemplo, 21 de septiembre de 2023 a las 9:00 a.m.

    graph = Graph(amount_nodes,amount_edges, market_cost)
    dictOfAction = {}
    for key in graph.nodes:
        dictOfAction[key] = []
    # Realizar la simulación
    # TODO: Use parallelism to make this more efficient 
    while hora_actual <= hora_inicial + duracion_simulacion:
        for person in graph.nodes.values():
            person.get_perception(graph)
            action = person.choose_action()
            person.energy -= 1
            person.make_action(action, graph.bipartite_graph)
            id = str(person)
            dictOfAction[int(id[len(id)-1])].append(DFActions(action, person))
        # Actualizar la hora actual
        hora_actual += paso_de_tiempo
    
    simulat = "Termino la simulacion"
    return simulat


def DFActions(action, person):
    if action == 0:
        return "ESTOY CAMINO AL HOSPITAL " + str(person)
    elif action == 1:
        return "ESTOY CAMINO AL MERCADO " + str(person)
    elif action == 2:
        return "ESTOY CAMINO AL TRABAJO " + str(person) 
    elif action == 3:
        return "ESTOY ESTUDIANDO " + str(person)
    elif action == 4:
        return "ESTOY DESCANSANDO " + str(person)
    elif action == 5:
        return "ESTOY PREVINIENDO " + str(person)