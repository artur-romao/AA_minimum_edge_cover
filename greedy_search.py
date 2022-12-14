import string
import os
import time
from Graph import Graph

probs = [0.125, 0.25, 0.5, 0.75]
letters = list(string.ascii_letters)

if not os.path.isdir("results"): 
    os.mkdir("results")

if not os.path.isdir("results/greedy"):
    os.mkdir("results/greedy")

for n_vertices in range(2, 52): # starting on 2 because the graph will be disconnected if there is only one vertice
    for prob in probs:
        graph = Graph(n_vertices, prob)
        graph.gen_graph("greedy")
        
        if len(graph.edges) == 0: # If no edges were generated, that means that the graph is invalid and that we should advance to the next iteration (or graph)
            continue
        
        file = open("results/greedy/greedy{}_{}.txt".format("".join(["0", str(graph.n_vertices)]), graph.prob), "w") if graph.n_vertices < 10 else open("results/greedy/greedy{}_{}.txt".format(graph.n_vertices, graph.prob), "w")
        file.write("No. vertices: {}\nProbability: {}\n".format(graph.n_vertices, graph.prob))

        adj_list = graph.gen_adjacency_list()
        vertices = sorted([v[0] for v in graph.connected_vertices])
        solution = []
        solution_vertices = []
        num_of_neighbours = [len(adj) for adj in adj_list] # This is a virtual list of the number of neighbours for each vertex that will be updated as the algorithm progresses
        num_of_basic_operations = 0
        solution_time = time.time() # Start counting the time of the solution

        while sorted(solution_vertices) != vertices:
            min_neighbours_vertice = num_of_neighbours.index(min(num_of_neighbours)) # Get the index of the vertex with the least number of neighbours that wasn't already added to the solution
            solution_vertices.append(vertices[min_neighbours_vertice]) # Add the vertex to the solution
            num_of_neighbours[min_neighbours_vertice] = 1000 # Set the number of neighbours to a high number so that it won't be chosen again
            get_real_num_of_neighbours = graph.get_list_with_num_of_neighbours() # Get the real number of neighbours for each vertex
            neighbours = [get_real_num_of_neighbours[vertices.index(vertex)] for vertex in adj_list[min_neighbours_vertice]] # Get the number of neighbours for each neighbour of the selected vertex
            min_num_of_neighbours_index = neighbours.index(min(neighbours)) # Get the index of the neighbour with the least number of neighbours
            min_num_of_neighbours_neighbour = adj_list[min_neighbours_vertice][min_num_of_neighbours_index] # Get the neighbour vertex with the least number of neighbours
            num_of_basic_operations += (9 + 2 * len(adj_list[min_neighbours_vertice]) + 5) # Considered assingments, array accesses, appends and function calls as basic operations
            
            if min_num_of_neighbours_neighbour not in solution_vertices: # If the neighbour with the least number of neighbours is not in the solution, add it
                solution_vertices.append(min_num_of_neighbours_neighbour)  # Add the vertice to the solution
                num_of_neighbours[vertices.index(min_num_of_neighbours_neighbour)] = 1000 # Set the number of neighbours to a high number so that it won't be chosen again
                num_of_basic_operations += 3
            solution.append((vertices[min_neighbours_vertice], min_num_of_neighbours_neighbour)) # Add the edge to the solution
            num_of_basic_operations += 2
        
        solution_time = time.time() - solution_time # Get the time of the solution
        file.write("Execution time: {:.8f}\nNo. basic operations: {}".format(float(solution_time), num_of_basic_operations))
        file.close()
        graph.aggregate_data("greedy")
        graph.plot_analysis_charts("greedy")

        # Sorry for the messy code, I was in a hurry and I didn't have time to rename the variables and make the code more readable
        # The heuristics for this greedy algorithm can be found explained in the report, but basicly are:
        # 1. Choose the vertex with the least number of neighbours
        # 2. Choose the neighbour with the least number of neighbours
        # 3. Repeat the process until all vertices are connected