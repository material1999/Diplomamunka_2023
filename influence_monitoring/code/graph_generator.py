import itertools
import random
import numpy as np
import os

vertex_num = 10
vertex_weight_mean = 0.5
vertex_weight_deviation = 0.2

edge_num = 20
edge_weight_mean = 0.5
edge_weight_deviation = 0.2

instances = 10

print()

for instance_num in range(instances):

    vertex_weights = np.random.normal(vertex_weight_mean, vertex_weight_deviation, vertex_num)
    #print(vertex_weights)
    #print()
    vertex_weights = np.where(vertex_weights > 1, vertex_weights % 1, vertex_weights)
    #print(vertex_weights)
    #print()
    vertex_weights = np.where(vertex_weights < 0, -vertex_weights % 1, vertex_weights)
    #print(vertex_weights)
    #print()

    edge_weights = np.random.normal(edge_weight_mean, edge_weight_deviation, edge_num)
    #print(edge_weights)
    #print()
    edge_weights = np.where(edge_weights > 1, edge_weights % 1, edge_weights)
    #print(vertex_weights)
    #print()
    edge_weights = np.where(edge_weights < 0, -edge_weights % 1, edge_weights)
    #print(edge_weights)
    #print()

    a = list(itertools.permutations(range(vertex_num), 2))
    #print(a)
    #print()

    edges = list()
    s = len(a)
    for i in range(edge_num):
        r = random.randrange(s - i)
        a[r], a[-1] = a[-1], a[r]
        x = a.pop()
        edges.append(x)

    #print(edges)
    #print()

    edges_path = "graph_input/" + str(instance_num + 1) + "/edges.txt"
    vertices_path = "graph_input/" + str(instance_num + 1) + "/vertices.txt"
    os.makedirs(os.path.dirname(edges_path), exist_ok=True)
    os.makedirs(os.path.dirname(vertices_path), exist_ok=True)

    with open(edges_path, "w") as edges_output, \
        open(vertices_path, "w") as vertices_output:
        for i in range(vertex_num):
            vertices_output.write(str(i) + ";" + str(vertex_weights[i]) + "\n")
        for i in range(edge_num):
            edges_output.write(str(edges[i][0]) + ";" + str(edges[i][1]) + ";" + str(edge_weights[i]) + "\n")

    print(instance_num + 1, "done")

print()