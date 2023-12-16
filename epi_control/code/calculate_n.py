import numpy as np
import networkx as nx
import json
from pytictoc import TicToc

graphs = 1080
instances = 100
cutoff = 2

t = TicToc()

runtimes_path = "runtimes/calculate_n.txt"
with open(runtimes_path, "w") as runtimes_output:
    runtimes_output.write("Runtimes (s) - instances: " + str(instances) + "\n")

# for graph_num in range(1, graphs + 1):

#for i in range(1, 11):
for i in range(1, 2):
    for graph_num in range(i, graphs + 1, 10):

        t.tic()
    
        vertices = list()
        edges = list()
        vertices_nx = list()
        edges_nx = list()

        edges_path = "graph_input/5/" + str(graph_num) + "/edges.txt"
        vertices_path = "graph_input/5/" + str(graph_num) + "/vertices.txt"

        with open(edges_path, "r") as edges_input, open(vertices_path, "r") as vertices_input:
            for line in edges_input:
                data = line.replace("\n", "").split(";")
                edges.append((int(data[0]), int(data[1]), float(data[2])))
                edges_nx.append((int(data[0]), int(data[1])))
            for line in vertices_input:
                data = line.replace("\n", "").split(";")
                vertices.append((int(data[0]), float(data[1])))
                vertices_nx.append(int(data[0]))

        max_dict = dict()

        for instance_num in range(1, instances + 1):

            print("graph:", graph_num, "---", "instance:", instance_num)

            edges_sampled = list()
            vertices_sampled = list()

            for edge in edges:
                w = edge[2]
                r = np.random.rand()
                if (r < w):
                    edges_sampled.append((int(edge[0]), int(edge[1])))

            for vertex in vertices:
                w = vertex[1]
                r = np.random.rand()
                if (r < w):
                    vertices_sampled.append(int(vertex[0]))

            G = nx.Graph()
            G.add_nodes_from(vertices_nx)
            G.add_edges_from(edges_sampled)

            for vertex in vertices:
                #print(vertex)
                max = 0
                for vertex_start in vertices_sampled:
                    max += len(list(nx.all_simple_paths(G, source=vertex_start, target=vertex[0], cutoff=cutoff)))
                if (vertex[0] not in max_dict or max > max_dict[vertex[0]]):
                    max_dict[vertex[0]] = max

        with open("results/n/5/" + str(graph_num) + ".txt", "w") as results_N:
            results_N.write(json.dumps(max_dict))

        runtime = t.tocvalue()
        print("Runtime:", runtime, "s")

        with open(runtimes_path, "a") as runtimes_output:
            runtimes_output.write(str(graph_num) + ": " + str(runtime) + "\n")