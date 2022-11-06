# @Author: Artur Romão
# @Email:  artur.romao@ua.pt

import random, string, os
import networkx as nx
import pandas as pd
import matplotlib.pyplot as plot

random.seed(98470)
class Graph:
    def __init__(self, n_vertices, prob):
        self.n_vertices = n_vertices # Number of vertices to generate
        self.prob = prob # Probability for the maximum number of edges
        self.vertices = [] # This list will decrease as the graph is generated and will be empty when all vertices are connected
        self.connected_vertices = [] # This list will be constructed as the graph is being generated
        self.edges = []
        self.letters = list(string.ascii_letters)

    def gen_vertice(self):
        v = self.letters[len(self.vertices)], (random.randint(1, 20), random.randint(1, 20))
        return self.gen_vertice() if v in self.vertices else v # Check if the vertice was already created, otherwise return it

    def gen_edge(self):
        if self.vertices: # If there are still vertices that are not connected to any other vertice
            indexes = self.gen_random_indexes(len(self.vertices)) 
            if len(self.vertices) == 1: # If there is only one vertice left to be connected
                self.connected_vertices.append(self.vertices[indexes[0]]) 
                return self.vertices.pop()[0], self.connected_vertices[indexes[1]][0] # Create an edge that connects the last vertice to a random vertice already connected, when this condition passes, we ensure that all vertices are connected 
            self.connected_vertices.extend([self.vertices[indexes[0]], self.vertices[indexes[1]]]) # Notify that the vertices are connected
            if indexes[0] > indexes[1]: # This condition was merely added to make sure that the indexes are in the correct order of being popped, I know this check could be done in a better way, but it's working :P
                return self.vertices.pop(indexes[0])[0], self.vertices.pop(indexes[1])[0] # Return a tuple which will be an edge and pop the vertices that were used to create the edge from the list of unconnected vertices
            return self.vertices.pop(indexes[0])[0], self.vertices.pop(indexes[1] - 1)[0]
        else: # If all vertices are connected, create a normal edge, selecting random vertices
            indexes = self.gen_random_indexes(len(self.connected_vertices))
            edge = self.connected_vertices[indexes[0]][0], self.connected_vertices[indexes[1]][0] # Create the edge
            inverted_edge = self.connected_vertices[indexes[1]][0], self.connected_vertices[indexes[0]][0] # Since this is an undirected graph, we also need to check if the complementary edge exists
            return self.gen_edge() if edge in self.edges or inverted_edge in self.edges else edge # Check if that edge was already created, return it if not

    def gen_graph(self, search_type):
        [self.vertices.append(self.gen_vertice()) for _ in range(self.n_vertices)]
        n_edges = int(self.prob * self.n_vertices * (self.n_vertices - 1) / 2) # Num of Edges = prob * Max Num of Edges (V(V-1)/2)
        if self.n_vertices - 1 <= n_edges <= (self.n_vertices * (self.n_vertices - 1) / 2): # Num of edges must be between the min and max number of possible edges [Min = V-1, Max = V(V-1)/2]
            [self.edges.append(self.gen_edge()) for _ in range(n_edges)] # Create the edges
            self.save_graph(search_type) # Save the graph in a png file

    def gen_random_indexes(self, v_length):
        if v_length > 1: 
            index_1 = random.randint(0, v_length - 1)
            index_2 = random.randint(0, v_length - 1)  
            while index_1 == index_2: # Make sure the indexes are different
                index_2 = random.randint(0, v_length - 1)
            return index_1, index_2
        else: # This edge case will only happen when there is only one vertice left to be connected which means that we should connect it to a random vertice that is already connected
            return 0, random.randint(0, len(self.connected_vertices) - 1)

    def gen_adjacency_matrix(self):
        v_list = sorted([v[0] for v in self.connected_vertices])
        matrix = [[0 for _ in range(len(v_list))] for _ in range(len(v_list))] # Initialize a 0s matrix VxV with V being the number of vertices

        for edge in self.edges:
            matrix[v_list.index(edge[0])][v_list.index(edge[1])] = 1 # Add 1 to the matrix in the position of the edge's first vertice
            matrix[v_list.index(edge[1])][v_list.index(edge[0])] = 1 # Add 1 to the matrix in the position of the edge's second vertice

        return matrix

    def gen_incidence_matrix(self):
        v_list = sorted([v[0] for v in self.connected_vertices])
        matrix = [[0 for _ in range(len(self.edges))] for _ in range(len(v_list))] # Intialize a 0s matrix VxE with V being the number of vertices and E the number of edges

        for i, edge in enumerate(self.edges):
            matrix[v_list.index(edge[0])][i] = 1 # Add 1 to the matrix in the position of the edge's first vertice
            matrix[v_list.index(edge[1])][i] = 1 # Add 1 to the matrix in the position of the edge's second vertice

        return matrix

    def gen_adjacency_list(self): # This method was created for the greedy algorithm which took benefit from the adjacency list to find the next vertice to be visited
        v_list = sorted([v[0] for v in self.connected_vertices])
        adjacency_list = [[] for _ in range(len(v_list))]

        for edge in self.edges:
            adjacency_list[v_list.index(edge[0])].append(edge[1])
            adjacency_list[v_list.index(edge[1])].append(edge[0])

        return adjacency_list

    def get_list_with_num_of_neighbours(self):
        return [len(neighbours) for neighbours in self.gen_adjacency_list()]


    def save_graph(self, search_type):
        vertices = sorted([v[0] for v in self.connected_vertices])
        G = nx.Graph()
        G.add_nodes_from(vertices)
        for edge in self.edges:
            G.add_edge(edge[0], edge[1])
        nx.draw(G, with_labels=True)
        # print(nx.min_edge_cover(G)) This function returns the minimum edge cover of the graph so you can use it to check whether the algorithm is working correctly
        plot.savefig("results/{}/{}_{}graph.png".format(search_type, self.n_vertices, self.prob))
        plot.close()

    def aggregate_data(self, search_type):
        if not os.path.isdir("results/aggregations"): 
            os.mkdir("results/aggregations")
        aggregation_file = open("results/aggregations/{}_aggregation.txt".format(search_type), "w")
        aggregation_file.write("num_of_vertices prob execution_time num_of_basic_operations")
        if search_type == "exhaustive":
            aggregation_file.write(" num_of_solutions")
        for file in sorted(os.listdir("results/{}".format(search_type))):
            if file.endswith(".txt"):
                with open("results/{}/{}".format(search_type, file), "r") as f:
                    data = f.read().splitlines()
                    if data == []:
                        continue
                    aggregation_file.write("\n{} {} {} {}".format(data[0].replace("No. vertices: ", ""), data[1].replace("Probability: ", ""), data[2].replace("Execution time: ", ""), data[3].replace("No. basic operations: ", "")))
                    if search_type == "exhaustive":
                        aggregation_file.write(" {}".format(data[4].replace("No. of solutions: ", "")))
        aggregation_file.close()

    def plot_analysis_charts(self, search_type):
        data = pd.read_csv("results/aggregations/{}_aggregation.txt".format(search_type), sep=" ")
        num_of_vertices = data["num_of_vertices"]
        prob = data["prob"]
        execution_time = data["execution_time"]
        num_of_basic_operations = data["num_of_basic_operations"]
        if search_type == "exhaustive":
            num_of_solutions = data["num_of_solutions"]
        
        plot.scatter(num_of_vertices[prob == 0.125], execution_time[prob == 0.125], c="r", marker="+", label="Probability for max num of edges 0.125")
        plot.scatter(num_of_vertices[prob == 0.25], execution_time[prob == 0.25], c="b", marker="o", label="Probability for max num of edges 0.25")
        plot.scatter(num_of_vertices[prob == 0.5], execution_time[prob == 0.5], c="g", marker="x", label="Probability for max num of edges 0.5")
        plot.scatter(num_of_vertices[prob == 0.75], execution_time[prob == 0.75], c="y", marker="v", label="Probability for max num of edges 0.75")
        
        plot.legend()
        plot.title("Execution time for {} search".format(search_type))
        plot.xlabel("Number of vertices")
        plot.ylabel("Execution time (seconds)")
        plot.savefig("results/aggregations/{}_execution_time.png".format(search_type))
        plot.clf()

        plot.scatter(num_of_vertices[prob == 0.125], num_of_basic_operations[prob == 0.125], c="r", marker="+", label="Probability for max num of edges 0.125")
        plot.scatter(num_of_vertices[prob == 0.25], num_of_basic_operations[prob == 0.25], c="b", marker="o", label="Probability for max num of edges 0.25")
        plot.scatter(num_of_vertices[prob == 0.5], num_of_basic_operations[prob == 0.5], c="g", marker="x", label="Probability for max num of edges 0.5")
        plot.scatter(num_of_vertices[prob == 0.75], num_of_basic_operations[prob == 0.75], c="y", marker="v", label="Probability for max num of edges 0.75")

        plot.legend()
        plot.title("Number of basic operations for {} search".format(search_type))
        plot.xlabel("Number of vertices")
        plot.ylabel("Number of basic operations")
        plot.savefig("results/aggregations/{}_basic_operations.png".format(search_type))
        plot.clf()

        if search_type == "exhaustive":
            plot.scatter(num_of_vertices[prob == 0.125], num_of_solutions[prob == 0.125], c="r", marker="+", label="Probability for max num of edges 0.125")
            plot.scatter(num_of_vertices[prob == 0.25], num_of_solutions[prob == 0.25], c="b", marker="o", label="Probability for max num of edges 0.25")
            plot.scatter(num_of_vertices[prob == 0.5], num_of_solutions[prob == 0.5], c="g", marker="x", label="Probability for max num of edges 0.5")
            plot.scatter(num_of_vertices[prob == 0.75], num_of_solutions[prob == 0.75], c="y", marker="v", label="Probability for max num of edges 0.75")

            plot.legend()
            plot.title("Number of found solutions for {} search".format(search_type))
            plot.xlabel("Number of vertices")
            plot.ylabel("Number of solutions")
            plot.savefig("results/aggregations/{}_solutions.png".format(search_type))
            plot.clf()