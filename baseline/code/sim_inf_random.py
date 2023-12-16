import numpy as np
from pytictoc import TicToc
import networkx as nx
import random

graphs = 1080
instances = 10000
is_directed = False
B = 50

print()
print("----------------------------------------------------------------------------------------------------")
print()

t = TicToc()

runtimes_path = "runtimes/sim_inf_random.txt"
with open(runtimes_path, "w") as runtimes_output:
    runtimes_output.write("Runtimes (s) - instances: " + str(instances) + "\n")

for graph_num in range(1, graphs + 1, 10):

    t.tic()
    
    vertices_to_delete = random.sample(range(1, 1000 + 1), B)

    edges_path = "graph_input/5/" + str(graph_num) + "/edges.txt"
    vertices_path = "graph_input/5/" + str(graph_num) + "/vertices.txt"

    with open(edges_path, "r") as edges_input, open(vertices_path, "r") as vertices_input:

        sum = 0

        for instance_num in range(instances):

            reachable = set()

            vertices = list()
            edges = list()
            vertices_start = list()

            print("graph", graph_num, "# instance:", instance_num + 1, "/", instances)

            edges_input.seek(0)
            vertices_input.seek(0)

            for line in edges_input:
                data = line.replace("\n", "").split(";")
                w = float(data[2])
                r = np.random.rand()
                if (r < w):
                    edges.append((int(data[0]), int(data[1])))
            for line in vertices_input:
                data = line.replace("\n", "").split(";")
                vertices.append(int(data[0]))
                w = float(data[1])
                r = np.random.rand()
                if (r < w):
                    vertices_start.append(int(data[0]))

            #'''
            edges_to_remove = list()

            for vertex in vertices_to_delete:
                for edge in edges:
                    if (edge[0] == vertex or edge[1] == vertex):
                        edges_to_remove.append(edge)
                #print(vertex)
                vertices.remove(vertex)

            edges = [e for e in edges if e not in edges_to_remove]
            #'''

            G = nx.Graph()
            G.add_nodes_from(vertices)
            G.add_edges_from(edges)

            for vertex in vertices_start:
                if vertex in G:
                    current = nx.descendants(G, vertex)
                    reachable.update(current)

            #print(reachable)
            sum += len(reachable)

        print("Average infection:", sum / instances)

        sim_inf_path = "results/sim_inf_random/5/" + str(graph_num) + ".txt"

        with open(sim_inf_path, "w") as sim_inf_output:
            sim_inf_output.write("Average infection: " + str(sum / instances) + "\n")

    print()
    print("----------------------------------------------------------------------------------------------------")
    print()

    runtime = t.tocvalue()
    print("Runtime:", runtime, "s")

    with open(runtimes_path, "a") as runtimes_output:
            runtimes_output.write(str(graph_num) + ": " + str(runtime) + "\n")