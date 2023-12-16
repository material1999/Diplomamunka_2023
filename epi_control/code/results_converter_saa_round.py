graphs = 1080

infections_list = list()

for graph_num in range(1, graphs + 1, 10):
    input_path = "results/sim_inf_saa_round/5/" + str(graph_num) + ".txt"
    output_path = "results/saa_round_final.txt"
    with open(input_path, "r") as results_input:
        for line in results_input:
            infections_list.append(line.split(": ")[1])

with open(output_path, "w") as results_output:
    for infection in infections_list:
        results_output.write(infection)