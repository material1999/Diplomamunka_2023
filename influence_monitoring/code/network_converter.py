import numpy as np
import os

vertex_weight_mean = 0.05

#graph_num = 1
graph_num = 1080
vertex_num = 1000

print()

for current in range(1, graph_num + 1):

    vertex_weights = np.random.uniform(0, 2 * vertex_weight_mean, vertex_num)
    #print(vertex_weights)
    #print()

    input_path = "networks/" + str(current) + "/edgeweighted.csv"

    edges_path = "graph_input/5/" + str(current) + "/edges.txt"
    vertices_path = "graph_input/5/" + str(current) + "/vertices.txt"

    os.makedirs(os.path.dirname(edges_path), exist_ok=True)
    os.makedirs(os.path.dirname(vertices_path), exist_ok=True)
    
    with open(input_path, "r") as edges_input, open(edges_path, "w") as edges_output:
        next(edges_input)
        for line in edges_input:
            edges_output.write(line)

    with open(vertices_path, "w") as vertices_output:
        for i in range(1, vertex_num + 1):
            vertices_output.write(str(i) + ";" + str(vertex_weights[i - 1]) + "\n")
    
    print(current, "done")

print()