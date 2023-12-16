graphs = 1080

for graph_num in range(1, graphs + 1, 10):
    input_path = "results/graph_sol_norm/5/" + str(graph_num) + ".sol"
    output_path = "results/graph_sol_norm_formatted/5/" + str(graph_num) + ".sol"
    nodes_list = list()
    with open(input_path, "r") as results_input, open(output_path, "w") as results_output:
        for line in results_input:
            if (line[0].isdigit() and line.split(" ")[1] == "1\n"):
                nodes_list.append(int(line.split(" ")[0]))
        nodes_list.sort()
        for node in nodes_list:
            results_output.write(str(node) + "\n")