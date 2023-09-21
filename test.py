from simulation.Graphs import *
from tools.graph_tools import find_cliques
p = "person"

graph = Graph(5,5,p)

print(f"The cliques are:")
print(find_cliques(graph))


print(graph.nodes)


print(graph.edges)


print("Bipartite graph")
print(graph.bipartite_graph.nodes_L)
