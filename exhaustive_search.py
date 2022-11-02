import networkx as nx
import matplotlib.pyplot as plot
import string
import math
from Graph import Graph

probs = [0.125, 0.25, 0.5, 0.75]
letters = list(string.ascii_letters)

for n_vertices in range(2, 30): # starting on 2 because the graph will be disconnected if there is only one vertice
    for prob in probs:
        graph = Graph(n_vertices, prob)
        graph.gen_graph()
        
        vertices = [v[0] for v in graph.connected_vertices]
        G = nx.Graph()
        G.add_nodes_from(vertices)
        for edge in graph.edges:
            G.add_edge(edge[0], edge[1])

        if len(graph.edges) == 0: # If no edges were generated, that means that the graph is invalid and that we should advance to the next iteration (or graph)
            continue
        sets = []
        for i in range(2 ** len(graph.edges)):
            sets.append([graph.edges[j] for j in range(len(graph.edges)) if (i & (1 << j))]) # Generate all possible sets of edges
        
        sets = [s for s in sets if len(s) == math.ceil(n_vertices / 2)]
        vertices = [letters[i] for i in range(n_vertices)]
        set_vertices = []
        for s in sets:
            for edge in s:
                set_vertices.extend([edge[0], edge[1]])
            set_vertices = sorted(list(set(set_vertices)))
            if set_vertices == vertices:
                print("solution", s)
                print(nx.min_edge_cover(G))
            else:
                print("Not a solution!")
            set_vertices = []