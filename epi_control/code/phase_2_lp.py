import numpy as np
from gurobipy import GRB
import json
from pytictoc import TicToc

graphs = 1080
instances = 1000

t = TicToc()

runtimes_path = "runtimes/phase_2_lp.txt"
with open(runtimes_path, "w") as runtimes_output:
    runtimes_output.write("Runtimes (s) - instances: " + str(instances) + "\n")

# for graph_num in range(1, graphs + 1):

#for i in range(1, 11):
for i in range(1, 2):
    for graph_num in range(i, graphs + 1, 10):

        t.tic()

        solutions_path = "results/phase_1_lp/5/" + str(instances) + "/" + str(graph_num) + ".sol"
                    
        vertices = list()
        edges = list()
        vertices_start = list()

        edges_path = "graph_input/5/" + str(graph_num) + "/edges.txt"
        vertices_path = "graph_input/5/" + str(graph_num) + "/vertices.txt"

        with open(edges_path, "r") as edges_input, open(vertices_path, "r") as vertices_input:
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

        x = list()
        y = list()
        X = list()
        Y = list()
        X_0 = list()

        with open(solutions_path, "r") as solutions_input:
            next(solutions_input)
            next(solutions_input)
            for line in solutions_input:
                data = line.replace("\n", "").split(" ")
                if (data[0].startswith("x")):
                    x.append((int(data[0].replace("x", "").replace("[", "").replace("]", "")) + 1,
                            float(data[1])))
                else:
                    y.append((int(data[0].split(",")[0].replace("y", "").replace("[", "")) + 1,
                            int(data[0].split(",")[1].replace("]", "")) + 1,
                            float(data[1])))
                    
        n_path = "results_n/5/" + str(graph_num) + ".txt"

        with open(n_path, "r") as results_n:
            n_string = results_n.readline()
        
        n_dict = json.loads(n_string)

        for vertex in x:
            if (vertex[1] == 0.0 or vertex[1] == 1.0):
                X.append(vertex)
            else:
                probability = 0
                if (n_dict[str(vertex[0])] != 0):
                    probability = min(1.0, 2 * vertex[1] * np.log2(4 * len(vertices) * instances * n_dict[str(vertex[0])]))

                r = np.random.rand()
                if (r < probability):
                    X.append((vertex[0], 1))
                else:
                    X.append((vertex[0], 0))
                    
        for y_item in y:
            if (y_item[2] >= 0.5):
                Y.append((y_item[0], y_item[1], 1))
            else:
                Y.append((y_item[0], y_item[1], 0))
        
        for X_item in X:
            if (X_item[1] == 1.0):
                X_0.append(X_item)

        print("graph:", graph_num, "---", "selected:", len(X_0))

        results_path = "results/phase_2_lp/5/" + str(instances) + "/" + str(graph_num) + ".sol"
        with open(results_path, "w") as results_output:
            for X_0_item in X_0:
                results_output.write(str(X_0_item[0]) + "\n")

        runtime = t.tocvalue()
        print("Runtime:", runtime, "s")

        with open(runtimes_path, "a") as runtimes_output:
            runtimes_output.write(str(graph_num) + ": " + str(runtime) + "\n")