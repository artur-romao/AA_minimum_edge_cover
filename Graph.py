# @Author: Artur Romão
# @Email:  artur.romao@ua.pt

import random, string

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
        return self.gen_vertice() if v in self.vertices else v # Maybe append the vertice to list right away?

    def gen_edge(self):
        if self.vertices:
            indexes = self.gen_random_indexes(len(self.vertices))
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
        index_1 = random.randint(0, v_length - 1)
        index_2 = random.randint(0, v_length - 1)  
        while index_1 == index_2: # Make sure the indexes are different
            index_2 = random.randint(0, v_length - 1)
        return index_1, index_2

    def gen_adjacency_matrix(self):
        v_list = [v[0] for v in self.connected_vertices]
        matrix = [[0 for _ in range(len(v_list))] for _ in range(len(v_list))] # Initialize a matrix VxV with 0s with V being the number of vertices

        for edge in self.edges:
            matrix[v_list.index(edge[0])][v_list.index(edge[1])] = 1 # Add 1 to the matrix in the position of the edge's first vertice
            matrix[v_list.index(edge[1])][v_list.index(edge[0])] = 1 # Add 1 to the matrix in the position of the edge's second vertice

        return matrix

    def gen_incidence_matrix(self):
        v_list = [v[0] for v in self.connected_vertices]
        matrix = [[0 for _ in range(len(self.edges))] for _ in range(len(v_list))]

        for i, edge in enumerate(self.edges):
            matrix[v_list.index(edge[0])][i] = 1 # Add 1 to the matrix in the position of the edge's first vertice
            matrix[v_list.index(edge[1])][i] = 1 # Add 1 to the matrix in the position of the edge's second vertice

        return matrix

if __name__ == "__main__":
    graph = Graph(10, 1)
    for _ in range(graph.n_vertices):
        graph.vertices.append(graph.gen_vertice())

    for _ in range(int(graph.n_vertices * graph.prob)):
        graph.edges.append(graph.gen_edge())

    print(sorted(graph.connected_vertices))
    print(graph.edges)
    
    graph.connected_vertices = sorted(graph.connected_vertices)

    [print(row) for row in graph.gen_adjacency_matrix()]
    print()
    [print(row) for row in graph.gen_incidence_matrix()]