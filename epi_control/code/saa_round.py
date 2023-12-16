import numpy as np
from gurobipy import GRB
import gurobipy as gp
from pytictoc import TicToc
import json

graphs = 1080
instances = 100
B = 50
iterations = 5

t = TicToc()

runtimes_path = "runtimes/saa_round.txt"
with open(runtimes_path, "w") as runtimes_output:
    runtimes_output.write("Runtimes (s) - instances: " + str(instances) + "\n")

# for graph_num in range(1, graphs + 1):

#for i in range(1, 11):
for i in range(1, 2):
    for graph_num in range(i, graphs + 1, 10):

        t.tic()
    
        vertices = list()
        edges = list()

        edges_path = "graph_input/5/" + str(graph_num) + "/edges.txt"
        vertices_path = "graph_input/5/" + str(graph_num) + "/vertices.txt"

        with open(edges_path, "r") as edges_input, open(vertices_path, "r") as vertices_input:
            for line in edges_input:
                data = line.replace("\n", "").split(";")
                edges.append((int(data[0]), int(data[1]), float(data[2])))
            for line in vertices_input:
                data = line.replace("\n", "").split(";")
                vertices.append((int(data[0]), float(data[1])))

        # modell létrehozása
        m = gp.Model('tempvacc')

        # (6)
        # csúcs változók hozzáadása
        x = m.addVars(len(vertices), lb=0.0, ub=1.0, vtype=GRB.CONTINUOUS, name="x")
        y = m.addVars(len(vertices), instances, lb=0.0, ub=1.0, vtype=GRB.CONTINUOUS, name="y")

        m.update()

        # megszorítások

        # (5)
        m.addConstr(x.sum() <= B)

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

            # (2)
            m.addConstrs(y[v - 1, instance_num - 1] <= 1 - x[v - 1] for v in list(zip(*vertices))[0])

            # (3)
            m.addConstrs(y[u - 1, instance_num - 1] >= y[w - 1, instance_num - 1] - x[u - 1] for (u, w) in edges_sampled)
            m.addConstrs(y[u - 1, instance_num - 1] >= y[w - 1, instance_num - 1] - x[u - 1] for (w, u) in edges_sampled)

            # (4)
            m.addConstrs(y[v - 1, instance_num - 1] == 1 - x[v - 1] for v in vertices_sampled)

        # (1)
        # célfüggvény
        obj = y.sum() / instances
        m.setObjective(obj, GRB.MINIMIZE)

        runtime = t.tocvalue()
        print("Runtime:", runtime, "s")

        with open(runtimes_path, "a") as runtimes_output:
            runtimes_output.write(str(graph_num) + " - model creation: " + str(runtime) + "\n")

        for iteration in range(1, iterations + 1):

            t.tic()

            m.reset()
            
            # optimális megoldás kiszámolása
            m.optimize()

            solutions_path = "results/saa_round/5/" + str(graph_num) + "_" + str(iteration) + ".sol"

            # eredmény kiírása fájlba
            m.write(solutions_path)

            ####################################################################################################

            x_ = list()
            y_ = list()
            X = list()
            Y = list()
            X_0 = list()

            with open(solutions_path, "r") as solutions_input:
                next(solutions_input)
                next(solutions_input)
                for line in solutions_input:
                    data = line.replace("\n", "").split(" ")
                    if (data[0].startswith("x")):
                        x_.append((int(data[0].replace("x", "").replace("[", "").replace("]", "")) + 1,
                                float(data[1])))
                    else:
                        y_.append((int(data[0].split(",")[0].replace("y", "").replace("[", "")) + 1,
                                int(data[0].split(",")[1].replace("]", "")) + 1,
                                float(data[1])))
                        
            n_path = "results/n/5/" + str(graph_num) + ".txt"

            with open(n_path, "r") as results_n:
                n_string = results_n.readline()
            
            n_dict = json.loads(n_string)

            for vertex in x_:
                if (vertex[1] == 0.0 or vertex[1] == 1.0):
                    X.append(vertex)
                else:
                    probability = 0
                    if (n_dict[str(vertex[0])] != 0):
                        #probability = min(1.0, 2 * vertex[1] * np.log2(4 * len(vertices) * instances * n_dict[str(vertex[0])]))
                        #probability = min(1.0, vertex[1] * 2 * np.log2(2 * n_dict[str(vertex[0])]))
                        probability = min(1.0, vertex[1] * np.log2(n_dict[str(vertex[0])]))

                    r = np.random.rand()
                    if (r < probability):
                        X.append((vertex[0], 1))
                    else:
                        X.append((vertex[0], 0))
                        
            for y_item in y_:
                if (y_item[2] >= 0.5):
                    Y.append((y_item[0], y_item[1], 1))
                else:
                    Y.append((y_item[0], y_item[1], 0))
            
            for X_item in X:
                if (X_item[1] == 1.0):
                    X_0.append(X_item)

            print("graph:", graph_num, "---", "selected:", len(X_0))

            vertices_not_zero = list()

            for X_0_item in X_0:
                vertices_not_zero.append(int(X_0_item[0]))
            
            print(vertices_not_zero)

            #for vertex_set_zero in range(1, 1000 + 1):
            for vertex_set_zero in list(zip(*vertices))[0]:
                if vertex_set_zero not in vertices_not_zero:
                    #print(vertex_set_zero)
                    m.addConstr(x[vertex_set_zero - 1] == 0.0)

            ####################################################################################################

            runtime = t.tocvalue()
            print("Runtime:", runtime, "s")

            with open(runtimes_path, "a") as runtimes_output:
                runtimes_output.write(str(graph_num) + " - iteration " + str(iteration) + 
                                      " - selected " + str(len(vertices_not_zero)) + ": " + str(runtime) + "\n")