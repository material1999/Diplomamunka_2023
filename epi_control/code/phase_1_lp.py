import numpy as np
from gurobipy import GRB
import gurobipy as gp
from pytictoc import TicToc

graphs = 1080
instances = 1000
B = 50

t = TicToc()

runtimes_path = "runtimes/phase_1_lp.txt"
with open(runtimes_path, "w") as runtimes_output:
    runtimes_output.write("Runtimes (s) - instances: " + str(instances) + "\n")

# for graph_num in range(1, graphs + 1):

for i in range(1, 11):
    for graph_num in range(i, graphs + 1, 10):

        t.tic()

        print(graph_num)
    
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

        # optimális megoldás kiszámolása
        m.optimize()

        # eredmény kiírása fájlba
        m.write("results/phase_1_lp/5/" + str(instances) +"/" + str(graph_num) + ".sol")

        runtime = t.tocvalue()
        print("Runtime:", runtime, "s")

        with open(runtimes_path, "a") as runtimes_output:
            runtimes_output.write(str(graph_num) + ": " + str(runtime) + "\n")