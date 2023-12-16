from unicodedata import name
import gurobipy as gp
from gurobipy import GRB
from pytictoc import TicToc

graphs = 1080
k = 50

print()
print("----------------------------------------------------------------------------------------------------")
print()

t = TicToc()

runtimes_path = "runtimes/phase_2_5_norm.txt"
with open(runtimes_path, "w") as runtimes_output:
    runtimes_output.write("Runtimes (s)\n")

#for i in range(1, 11):
    #for graph_num in range(i, graphs + 1, 10):

#for graph_num in range(graphs):
#for graph_num in range(1, 2):
#for graph_num in range(1, graphs + 1):

for i in range(1, 2):
    for graph_num in range(i, graphs + 1, 10):

        t.tic()
        
        edges_path = "results/graph_flow_norm/5/" + str(graph_num) + ".txt"
        
        nodes = set()
        multidict_input = dict()
        from_source = list()

        with open(edges_path, "r") as input:
            
            for line in input:
                line = line.replace("\n", "")
                #print(line)
                parts = line.split(";")

                nodes.add(str(parts[0]))
                nodes.add(str(parts[1]))
    
                multidict_input[str(parts[0]), str(parts[1])] = float(parts[2])

                if parts[0] == 's':
                    from_source.append(parts[1])

        arcs, capacity = gp.multidict(multidict_input)

        N = len(nodes)
        #N = 100000000000000

        '''
        print()
        print("----------------------------------------------------------------------------------------------------")
        print()
        print(nodes)
        print()
        print(arcs)
        print()
        print(capacity)
        print()
        print("----------------------------------------------------------------------------------------------------")
        print()
        '''

        # modell létrehozása
        m = gp.Model('graph_flow')

        # változók hozzáadása
        flow = m.addVars(arcs, lb=0, vtype=GRB.CONTINUOUS, name="flow")
        #flow = m.addVars(arcs, name="flow")
        m.update()

        # kapacitások megszorításai
        m.addConstrs((flow.sum(i, j) <= capacity[i, j] for i, j in arcs), "cap")

        # csúcsokban a megmaradás törvénye
        m.addConstrs((flow.sum('*', i) == flow.sum(i, '*') for i in nodes if i != "s" and i != "t"), "node")

        # k darab irányba indulhat el fertőzés
        k_expr = 0

        for node in from_source:
            var_new = m.addVar(vtype=GRB.BINARY, name=node)
            m.update()
            tup = ('s', node)
            #print(flow.get(tup))
            var_old = flow.get(tup)
            #print(var_old)
            #print(var_new)
            m.addConstr(var_old * N >= var_new, name="extra_"+node+"(1)")
            m.addConstr(var_old <= var_new * N, name="extra_"+node+"(2)")
            k_expr += var_new
        
        m.addConstr(k_expr <= k)

        # célfüggvény
        obj = (flow.sum('*', 't'))
        m.setObjective(obj, GRB.MAXIMIZE)

        # optimális megoldás kiszámolása
        m.optimize()

        # eredmény kiírása fájlba
        m.write("results/graph_sol_norm/5/" + str(graph_num) + ".sol")

        '''
        print()
        print("----------------------------------------------------------------------------------------------------")
        print()
        
        # eredmények kiíratása
        if m.Status == GRB.OPTIMAL:
            solution = m.getAttr('X', flow)
            for i, j in arcs:
                if solution[i, j] > 0:
                    print('%s -> %s: %g' % (i, j, solution[i, j]))
        '''
        
        '''
        print()
        print("----------------------------------------------------------------------------------------------------")
        print()

        for item in m.getVars():
            print(item)
        '''

        print()
        print("----------------------------------------------------------------------------------------------------")
        print()

        runtime = t.tocvalue()
        print("Runtime:", runtime, "s")

        with open(runtimes_path, "a") as runtimes_output:
            runtimes_output.write(str(graph_num) + ": " + str(runtime) + "\n")