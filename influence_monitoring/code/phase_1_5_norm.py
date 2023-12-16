import igraph as ig
import numpy as np
from pytictoc import TicToc

graphs = 1080
instances = 10000

print()
print("----------------------------------------------------------------------------------------------------")
print()

t = TicToc()

runtimes_path = "runtimes/phase_1_5_norm.txt"
with open(runtimes_path, "w") as runtimes_output:
    runtimes_output.write("Runtimes (s) - instances: " + str(instances) + "\n")

#for i in range(1, 11):
    #for graph_num in range(i, graphs + 1, 10):

#for graph_num in range(graphs):
#for graph_num in range(1, graphs + 1):

for i in range(1, 2):
    for graph_num in range(1, graphs + 1, 10):
    
        t.tic()
        
        vertices = list()
        edges = list()

        edges_path = "graph_input/5/" + str(graph_num) + "/edges.txt"
        vertices_path = "graph_input/5/" + str(graph_num) + "/vertices.txt"

        with open(edges_path, "r") as edges_input, open(vertices_path, "r") as vertices_input:
            for line in edges_input:
                data = line.replace("\n", "").split(";")
                edges.append((int(data[0]), int(data[1]), float(data[2])))
            #print(edges)
            #print()
            for line in vertices_input:
                data = line.replace("\n", "").split(";")
                vertices.append((int(data[0]), float(data[1])))
            #print(vertices)
            #print()

        apriori = [num[1] for num in vertices]

        g = ig.Graph.TupleList(edges, True, edge_attrs="weight")
        g.vs["infected"] = [0] * len(g.vs)
        g.vs["apriori"] = apriori
        g.vs["level"] = [-1] * len(g.vs)
        g.vs["new_weight"] = [1.0] * len(g.vs)
        #g.vs["label"] = [round(num, 3) for num in g.vs["apriori"]]
        g.vs["label"] = g.vs["name"]
        g.vs["color"] = ["cyan"] * len(g.vs)

        g.es["label"] = [round(num, 3) for num in g.es["weight"]]
        g.es["new_weight"] = [0.0] * len(g.es)

        #layout = g.layout("drl")
        #layout = g.layout("large")

        #ig.plot(g, layout=layout)

        '''
        print(g)
        '''

        '''
        print()
        print("----------------------------------------------------------------------------------------------------")
        print()
        '''

        edge_weight_sum_dict = dict()
        vertex_weight_sum_dict = dict()
        vertex_in_instance_dict = dict()

        for instance_num in range(instances):

            g_curr = g.copy()

            edges_to_delete = list()

            for edge in g_curr.es:
                w = edge["weight"]
                r = np.random.rand()
                #print("random:", r, ", weight:", w)
                if (r >= w):
                    edges_to_delete.append(edge)
                    #print("deleted")

            g_curr.delete_edges(edges_to_delete)

            for vertex in g_curr.vs:
                a = vertex["apriori"]
                r = np.random.rand()
                #print("random:", r, ", apriori:", w)
                if (r <= a):
                    vertex["infected"] = 1
                    vertex["color"] = "red"
                    #print("infected")

            #ig.plot(g_curr, layout=layout)

            '''
            print(g_curr)
            '''

            '''
            print()
            print("----------------------------------------------------------------------------------------------------")
            print()
            '''

            for vertex in g_curr.vs:
                if vertex["infected"] == 1:
                    vertex["level"] = 0

            '''
            for vertex in g_curr.vs:
                print(vertex)
            '''

            #print([v["name"] for v in g_curr.vs if v["level"] == 0])
            '''
            print()
            print("----------------------------------------------------------------------------------------------------")
            print()
            '''

            new_infected = 1
            level = 0
            while(new_infected > 0):
                new_infected = 0
                '''
                print("##########", level, "-->", level + 1, "##########")
                print()
                '''
                for v in [vertex for vertex in g_curr.vs if vertex["level"] == level]:
                    #print(v)
                    #print(v.out_edges())
                    for e in [edge for edge in v.out_edges() if g_curr.vs[edge.target]["color"] == "cyan"]:
                        '''
                        print(v["name"], "-->", g_curr.vs[e.target]["name"])
                        '''
                        #g_curr.vs[e.target]["color"] = "yellow"
                        g_curr.vs[e.target]["level"] = level + 1
                        new_infected += 1

                level += 1

                for v in g_curr.vs:
                    if v["level"] > 0 and v["color"] != "yellow":
                        v["color"] = "yellow"

                '''
                print()
                for vertex in g_curr.vs:
                    print(vertex)
                '''
                
                '''
                if new_infected == 0:
                    print("no more edges to draw")
                else:
                    #ig.plot(g_curr, layout=layout)
                    pass
                '''

            edges_to_delete = list()
            for edge in g_curr.es:
                if g_curr.vs[edge.source]["level"] >= g_curr.vs[edge.target]["level"] or g_curr.vs[edge.source]["level"] == -1:
                    edges_to_delete.append(edge)
            g_curr.delete_edges(edges_to_delete)

            #ig.plot(g_curr, layout=layout)

            vertices_to_delete = list()
            for vertex in g_curr.vs:
                if vertex["level"] == -1 or vertex.degree() == 0:
                    vertices_to_delete.append(vertex)
            g_curr.delete_vertices(vertices_to_delete)

            ##ig.plot(g_curr, layout=layout)

            '''
            print()
            print("----------------------------------------------------------------------------------------------------")
            print()
            '''
            
            '''
            for vertex in g_curr.vs:
                print(vertex)
            '''

            '''
            print()
            print("----------------------------------------------------------------------------------------------------")
            print()
            '''

            '''
            for edge in g_curr.es:
                print(edge)
            '''

            '''
            print()
            print("----------------------------------------------------------------------------------------------------")
            print()
            '''

            if g_curr.vs:
                max_level = max(g_curr.vs["level"])
            else:
                max_level = 0
            
            '''
            print("max level:", max_level)
            print()
            '''

            for l in range(max_level, 0, -1):
                '''
                print("level:", l)
                '''
                for v in [vertex for vertex in g_curr.vs if vertex["level"] == l]:
                    in_edge_list = [edge for edge in v.in_edges() if g_curr.vs[edge.target] == v]
                    new_edge_weight = v["new_weight"] / len(in_edge_list)
                    for e in in_edge_list:
                        '''
                        print(v["name"], "(", new_edge_weight, ")", "<--", e["weight"])
                        '''
                        e["new_weight"] = new_edge_weight
                
                '''
                print()
                print("----------------------------------------------------------------------------------------------------")
                print()
                '''

                '''
                for edge in g_curr.es:
                    print(edge)
                '''

                '''
                print()
                print("----------------------------------------------------------------------------------------------------")
                print()
                '''

                for v in [vertex for vertex in g_curr.vs if vertex["level"] == l - 1]:
                    new_vertex_weight = 1.0
                    for e in v.out_edges():
                        new_vertex_weight += e["new_weight"]
                    v["new_weight"] = new_vertex_weight

                '''
                for vertex in g_curr.vs:
                    print(vertex)
                '''

                '''
                print()
                print("----------------------------------------------------------------------------------------------------")
                print()
                '''

            
            # élek felvétele a dict-be, ha még nincs, ha pedig már van, akkor hozzáadni új elemként
            # kulcs: HONNAN;HOVA
            # érték: az adott él súlyát hozzáadni

            for edge in g_curr.es:
                edge_name = str(g_curr.vs[edge.source]["name"]) + ";" + str(g_curr.vs[edge.target]["name"])
                if edge_name in edge_weight_sum_dict:
                    edge_weight_sum_dict[edge_name] += edge["new_weight"]
                    '''
                    print("added to old: " + str(edge["new_weight"]))
                    '''
                else:
                    edge_weight_sum_dict[edge_name] = edge["new_weight"]
                    '''
                    print("new added with: " + str(edge["new_weight"]))
                    '''

            '''
            print()
            print(edge_weight_sum_dict)
            print()
            print("----------------------------------------------------------------------------------------------------")
            print()
            '''

            # csúcsok felvétele a dict-be, ha még nincs, ha pedig már van, akkor hozzáadni új elemként
            # kulcs: CSÚCS
            # érték: az adott csúcs súlyát hozzáadni

            for vertex in g_curr.vs:
                vertex_name = str(vertex["name"])
                if vertex_name in vertex_weight_sum_dict:
                    vertex_weight_sum_dict[vertex_name] += vertex["new_weight"]
                    '''
                    print("added to old: " + str(edge["new_weight"]))
                    '''
                else:
                    vertex_weight_sum_dict[vertex_name] = vertex["new_weight"]
                    '''
                    print("new added with: " + str(edge["new_weight"]))
                    '''

            '''
            print()
            print(vertex_weight_sum_dict)
            print()
            print("----------------------------------------------------------------------------------------------------")
            print()
            '''

            # csúcsok megszámolása, mennyi instance-ban vannak benne
            for vertex in g_curr.vs:
                vertex_name = vertex["name"]
                if vertex_name in vertex_in_instance_dict:
                    vertex_in_instance_dict[vertex_name] += 1
                else:
                    vertex_in_instance_dict[vertex_name] = 1

            '''
            print()
            print(vertex_in_instance_dict)
            print()
            print("----------------------------------------------------------------------------------------------------")
            print()
            '''

            g_curr.es["label"] = g_curr.es["new_weight"]
            #ig.plot(g_curr, layout=layout)

            #g_curr.vs["label"] = g_curr.vs["new_weight"]
            #ig.plot(g_curr, layout=layout)
            print("graph", graph_num, "# instance:", instance_num + 1, "/", instances)


        # átlagolás, vertex dict-ben minden kulcshoz tartozó értéket oszatni az instance-ok számával

        for k, v in vertex_weight_sum_dict.items():
            vertex_weight_sum_dict[k] = v / instances

        '''
        print("Final vertices:")
        print(vertex_weight_sum_dict)
        print()
        print("----------------------------------------------------------------------------------------------------")
        print()
        '''

        # maximális vertex weight kiszámolása
        max_vertex_weight = vertex_weight_sum_dict[max(vertex_weight_sum_dict, key=vertex_weight_sum_dict.get)]
        # print(max_vertex_weight)

        # átlagolás és normálás, edge dict-ben minden kulcshoz tartozó értéket oszatni az instance-ok számával és
        # a maximális vertex weight-tel

        for k, v in edge_weight_sum_dict.items():
            edge_weight_sum_dict[k] = v / instances / max_vertex_weight

        '''
        print("Final edges:")
        print(edge_weight_sum_dict)
        print()
        print("----------------------------------------------------------------------------------------------------")
        print()
        '''

        # átlagolás, vertex dict-ben minden kulcshoz tartozó értéket oszatni az instance-ok számával

        for k, v in vertex_in_instance_dict.items():
            vertex_in_instance_dict[k] = v / instances
        
        '''
        print("Vertex appearances:")
        print(vertex_in_instance_dict)
        print()
        print("----------------------------------------------------------------------------------------------------")
        print()
        '''

        # kiinduló csúcs + élek

        for k, v in vertex_in_instance_dict.items():
            sum = 0
            for k_, v_ in edge_weight_sum_dict.items():
                if str(k_).split(";")[0] == str(k):
                    sum += v_
            if sum > 0:
                new_edge_name = "s;" + str(k)
                edge_weight_sum_dict[new_edge_name] = sum / max_vertex_weight
        
        '''
        print("source added")
        print(edge_weight_sum_dict)
        print()
        print("----------------------------------------------------------------------------------------------------")
        print()
        '''

        # nyelő csúcs + élek

        for k, v in vertex_in_instance_dict.items():
            new_edge_name = str(k) + ";t"
            edge_weight_sum_dict[new_edge_name] = v / max_vertex_weight

        '''
        print("target added")
        print(edge_weight_sum_dict)
        print()
        print("----------------------------------------------------------------------------------------------------")
        print()
        '''

        # kiírás fájlba szokásos módon: HONNAN;HOVA;ÉLSÚLY

        graph_flow_path = "results/graph_flow_norm/5/" + str(graph_num) + ".txt"
        with open(graph_flow_path, "w") as graph_flow_output:
            for k, v in edge_weight_sum_dict.items():
                graph_flow_output.write(str(k) + ";" + str(v) + "\n")

        '''
        print("writing done")
        print()
        print("----------------------------------------------------------------------------------------------------")
        print()
        '''

        runtime = t.tocvalue()
        print("Runtime:", runtime, "s")

        with open(runtimes_path, "a") as runtimes_output:
            runtimes_output.write(str(graph_num) + ": " + str(runtime) + "\n")

        print()
        print("----------------------------------------------------------------------------------------------------")
        print()