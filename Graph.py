# @Author: Artur Romão
# @Email:  artur.romao@ua.pt

import random, string
import networkx as nx
import matplotlib.pyplot as plot

class Graph:
    def __init__(self, n_vertices, prob):
        self.n_vertices = n_vertices # Number of vertices to generate
        self.prob = prob # Probability for the maximum number of edges
        self.vertices = []
        self.connected_vertices = []
        self.edges = []
        self.letters = list(string.ascii_letters)
        random.seed(98470)

    def gen_vertice(self):
        v = self.letters[len(self.vertices)], (random.randint(1, 20), random.randint(1, 20))
        return self.gen_vertice() if v in self.vertices else v

    def gen_edge(self):
        if self.vertices:
            indexes = self.gen_random_indexes(len(self.vertices))
            if len(self.vertices) == 1:
                self.connected_vertices.append(self.vertices[indexes[0]])
                return self.vertices.pop()[0], self.connected_vertices[indexes[1]][0]
            self.connected_vertices.extend([self.vertices[indexes[0]], self.vertices[indexes[1]]])
            if indexes[0] > indexes[1]:
                return self.vertices.pop(indexes[0])[0], self.vertices.pop(indexes[1])[0]
            return self.vertices.pop(indexes[0])[0], self.vertices.pop(indexes[1] - 1)[0]
        else:
            indexes = self.gen_random_indexes(len(self.connected_vertices))
            edge = self.connected_vertices[indexes[0]][0], self.connected_vertices[indexes[1]][0] # Create the edge
            inverted_edge = self.connected_vertices[indexes[1]][0], self.connected_vertices[indexes[0]][0] # Since this is an undirected graph, we also need to check if the complementary edge exists
            return self.gen_edge() if edge in self.edges or inverted_edge in self.edges else edge # Check if any of the edges were already created

    def gen_random_indexes(self, v_length):
        if v_length > 1: 
            index_1 = random.randint(0, v_length - 1)
            index_2 = random.randint(0, v_length - 1)  
            while index_1 == index_2: # Make sure the indexes are different
                index_2 = random.randint(0, v_length - 1)
            return index_1, index_2
        else: # This edge case will only happen when there is only one vertice left in list "vertices" which means that we should connect it to a vertice in list "connected_vertices"
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

    def gen_adjacency_list(self):
        v_list = sorted([v[0] for v in self.connected_vertices])
        adjacency_list = [[] for _ in range(len(v_list))]

        for edge in self.edges:
            adjacency_list[v_list.index(edge[0])].append(edge[1])
            adjacency_list[v_list.index(edge[1])].append(edge[0])

        return adjacency_list

    def get_list_with_num_of_neighbours(self):
        return [len(neighbours) for neighbours in self.gen_adjacency_list()]

    def gen_graph(self):
        [self.vertices.append(self.gen_vertice()) for _ in range(self.n_vertices)]
        n_edges = int(self.prob * self.n_vertices * (self.n_vertices - 1) / 2) # Num of Edges = prob * Max Num of Edges
        print(f"n_vertices: {self.n_vertices}, prob: {self.prob}, n_edges: {n_edges}")
        if self.n_vertices - 1 <= n_edges <= (self.n_vertices * (self.n_vertices - 1) / 2): # Num of edges must be between the min and max number of possible edges
            print("Generating graph...")
            [self.edges.append(self.gen_edge()) for _ in range(n_edges)]
            print("Graph generated!")
            self.plot_graph()
        else:
            print("Invalid number of edges")

    def plot_graph(self):
        vertices = sorted([v[0] for v in self.connected_vertices])
        print(f"Vertices: {vertices}")
        G = nx.Graph()
        G.add_nodes_from(vertices)
        for edge in self.edges:
            G.add_edge(edge[0], edge[1])
        nx.draw(G, with_labels=True)
        # print(nx.min_edge_cover(G))
        plot.show()

if __name__ == "__main__":
    graph = Graph(10, 1)
    for _ in range(graph.n_vertices):
        graph.vertices.append(graph.gen_vertice())

    for _ in range(int(graph.n_vertices * graph.prob)):
        graph.edges.append(graph.gen_edge())

    print(sorted(graph.connected_vertices))
    print(graph.edges)
    
    graph.connected_vertices = sorted(graph.connected_vertices)

    print("\nAdjacency Matrix:")
    [print(row) for row in graph.gen_adjacency_matrix()]
    print("\nIncidence Matrix:")
    [print(row) for row in graph.gen_incidence_matrix()]

    print(graph.gen_incidence_matrix()[1][5])
    graph.plot_graph()