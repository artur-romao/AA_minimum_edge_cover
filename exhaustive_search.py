import os
import string
import math
import time
import itertools
from Graph import Graph

probs = [0.125, 0.25, 0.5, 0.75]
letters = list(string.ascii_letters)

if not os.path.isdir("results"): 
    os.mkdir("results")

if not os.path.isdir("results/exhaustive"):
    os.mkdir("results/exhaustive")

for n_vertices in range(2, 30): # starting on 2 because the graph will be disconnected if there is only one vertice
    for prob in probs:
        graph = Graph(n_vertices, prob)
        graph.gen_graph("exhaustive")

        if len(graph.edges) == 0: # If no edges were generated, that means that the graph is invalid and that we should advance to the next iteration (or graph)
            continue
        
        file = open("results/exhaustive/exhaustive{}_{}.txt".format("".join(["0", str(graph.n_vertices)]), graph.prob), "w") if graph.n_vertices < 10 else open("results/exhaustive/exhaustive{}_{}.txt".format(graph.n_vertices, graph.prob), "w")
        file.write("No. vertices: {}\nProbability: {}\n".format(graph.n_vertices, graph.prob))
        # sets = list(itertools.combinations(graph.edges, math.ceil(len(graph.edges) / 2))) This is an alternative to the code below but it didn't work as expected
        number_of_basic_operations = 0
        sets = []
        for i in range(2 ** len(graph.edges)):
            sets.append([graph.edges[j] for j in range(len(graph.edges)) if (i & (1 << j))]) # Generate all possible sets of edges
            number_of_basic_operations += 1
        sets = [s for s in sets if len(s) == math.ceil(n_vertices / 2)] # Filter the list to only include sets with the correct number of edges, according to this website: https://www.geeksforgeeks.org/program-to-calculate-the-edge-cover-of-a-graph/
        vertices = [letters[i] for i in range(n_vertices)]
        set_vertices = []
        number_of_solutions = 0
        solution_time = time.time() # Start counting the time of the solution
        for s in sets:
            for edge in s:
                set_vertices.extend([edge[0], edge[1]]) # Add the vertices of each edge to the set of vertices
                number_of_basic_operations += 3 # 3 because extending the array is a basic operation and accessing the vertices of the edge is also a basic operation
            set_vertices = sorted(list(set(set_vertices))) # Remove duplicates and sort the list
            if set_vertices == vertices: # When all vertices are in the set, that means that the set is a solution
                number_of_solutions += 1
                number_of_basic_operations += 1 # 1 because adding to the number of solutions is a basic operation   
            number_of_basic_operations += 1 # 1 because comparing the lists is a basic operation
            set_vertices = [] # Reset the set of vertices for the next iteration
        solution_time = time.time() - solution_time # Get the time of the solution
        file.write("Execution time: {:.8f}\nNo. basic operations: {}\nNo. of solutions: {}".format(float(solution_time), number_of_basic_operations, number_of_solutions))
        file.close()
        graph.aggregate_data("exhaustive")
        graph.plot_analysis_charts("exhaustive")