import multiprocessing
from multiprocessing import Queue
from queue import Empty
import datetime
from graph_world.Graphs_m import Graph_m, Bipartite_Graph
import time




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
    
def action_per_person(graph: Graph_m,person):
    person.get_perception(graph)
    action = person.choose_action()
    person.energy -= 1
    person.make_action(action, graph.bipartite_graph)
    id = str(person)
    # dictOfAction[int(id[len(id)-1])].append(DFActions(action, person))
    # print(f"{person} proceso: {i} ", end = "")
    proceso_actual = multiprocessing.current_process().name
    # print(f"{person} proceso: {proceso_actual}... ")
    # return int(id[len(id)-1]), DFActions(action,person)
    
# def worker(graph,queue:Queue,i,dictOfAction):
#     """
#     Toma un ítem de la cola y descarga su contenido,
#     hasta que la misma se encuentre vacía.
#     """
#     while True:
#         try:
#             person = queue.get_nowait()
#         except Empty:
#             break
#         else:
#             action_per_person(graph,person,i,dictOfAction)



# def action_for_person(graph: Graph, hora_actual, hora_inicial, duracion_simulacion, paso_de_tiempo, queue:Queue, k):
#     dictOfAction = {}
#     contin = True
#     for key in graph.nodes:
#         dictOfAction[key] = []
#     # while hora_actual <= hora_inicial + duracion_simulacion:
#     count = 0
#     while contin:
#         person = queue.get_nowait()
#         person.get_perception(graph)
#         action = person.choose_action()
#         person.energy -= 1
#         person.make_action(action, graph.bipartite_graph)
#         id = str(person)
#         dictOfAction[int(id[len(id)-1])].append(DFActions(action, person))
#         # queue.put(person)
#         count += 1
#         if count == len(graph.nodes):
#             contin = False
        
#         print(f"{person} process {k}")
        
#     print("Llegue a aumentar la hora")
#     hora_actual += paso_de_tiempo
#     return f"Termino el proceso {k}"


def main():
    amount_nodes, amount_edges, market_cost = 5, 5, 240
        # Definir la duración de la simulación
    duracion_simulacion = datetime.timedelta(hours = 5)

    hora_inicial = datetime.datetime(2023, 10, 22, 10, 0)

    # Definir el paso de tiempo
    paso_de_tiempo = datetime.timedelta(hours = 1)

    # Definir la hora de inicio de la simulación
    hora_actual = datetime.datetime(2023, 10, 22, 10, 0)  

    graph = Graph_m(amount_nodes,amount_edges, market_cost)
    dictOfAction = {}
    for key in graph.nodes:
        dictOfAction[key] = []
    # Realizar la simulación
    # TODO: Use parallelism to make this more efficient.
    # processes = []
    # queue = Queue(amount_nodes)
    # for person in graph.nodes.values():
    #     queue.put(person)
    start = time.time()
    pool = multiprocessing.Pool(processes=3)
    while hora_actual <= hora_inicial + duracion_simulacion:
        resultados = pool.starmap(action_per_person, [(graph,person) for person in graph.nodes.values()])
        
        hora_actual += paso_de_tiempo
    pool.close()
    pool.join()

    
    #     proc = [True, True, True]
    

        # for i in range(3):
        #     processes.append(multiprocessing.Pool(target = worker,args=(graph,queue,i,dictOfAction)))
        #     processes[i].start()
        #     print("Proceso %d lanzado." % (i))
    # while proc:
    #     for i in range(3):
    #         if processes[i].is_alive():
    #             continue
    #         else:
    #             proc[i] = False
    #     if all(proc):
    #         break
    #     hora_actual += paso_de_tiempo
    # for process in processes:
    #     process.join()


        

    
    
        # for person in graph.nodes.values():
        #     person.get_perception(graph)
        #     action = person.choose_action()
        #     person.energy -= 1
        #     person.make_action(action, graph.bipartite_graph)
        #     id = str(person)
        #     dictOfAction[int(id[len(id)-1])].append(DFActions(action, person))
        # Actualizar la hora actual
        # hora_actual += paso_de_tiempo
    end = time.time()
    print(f"Tiempo con paralelismo {end - start}")
    print("La ejecución termino.")
    # simulat = "Termino la simulacion"
    # return simulat

if __name__ == "__main__":
    main()