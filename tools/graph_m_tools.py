


def find_cliques(graph):
    cliques = []
    potential_clique = set(graph.nodes)
    candidates = set(graph.nodes)
    visited = set()

    def Bron_Kerbosch(R, P, X):
        if len(P) == 0 and len(X) == 0:
            cliques.append(R)
            return

        for node in list(P):
            neighbors = set(graph.edges[node])
            Bron_Kerbosch(R.union([node]), P.intersection(neighbors), X.intersection(neighbors))

            P.remove(node)
            X.add(node)

    for node in list(candidates):
        neighbors = set(graph.edges[node])
        Bron_Kerbosch(set([node]), potential_clique.intersection(neighbors), set())

        candidates.remove(node)
        visited.add(node)

    return cliques