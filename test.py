# from graph_world.Graphs import *
# from tools.graph_tools import find_cliques
from simulation.dinamic_control_dengue import run_simulation
# p = "person"

# graph = Graph(5,5)

# print(f"The cliques are:")
# print(find_cliques(graph))


# print(graph.nodes)


# print(graph.edges)


# print("Bipartite graph")
# print(graph.bipartite_graph.edges)

# places = graph.bipartite_graph.find_place("Hospital")

# print(places)

simulation = run_simulation(5,5,250)

print(simulation)

# edge = graph.bipartite_graph.edges[0]
# repl = graph.bipartite_graph.edges[1]
# item = next(iter(edge))
# item2 = next(iter(repl))
# print(str(item) + " " + str(item2))
# list_edges = [(0,item,item2)]

# graph.bipartite_graph.replace_edges(list_edges)

# print(graph.bipartite_graph.edges)