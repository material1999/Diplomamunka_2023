graphs = 1080

for graph_num in range(1, graphs + 1, 10):
    input_path = "results/phase_1_ip/5/" + str(graph_num) + ".sol"
    output_path = "results/phase_1_ip_formatted/5/" + str(graph_num) + ".sol"
    nodes_list = list()
    with open(input_path, "r") as results_input, open(output_path, "w") as results_output:
        for line in results_input:
            if (line[0] == "x" and line.split(" ")[1] != "0\n"):
                nodes_list.append(int(line.split(" ")[0].split("[")[1].split("]")[0]))
        nodes_list.sort()
        for node in nodes_list:
            results_output.write(str(node + 1) + "\n")