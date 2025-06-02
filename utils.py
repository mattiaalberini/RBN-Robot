import random


# Lettore parametri da file
def read_file(file_name):
    parameters_app = {}

    with open(file_name, "r", encoding="utf-8") as file:
        for line in file:
            if ":" in line:
                parameters_app[line.split(":")[0].strip()] = line.split(":")[1].strip()

    return parameters_app


# Generatore valori booleani random
def generate_random_boolean_values(n_output, bias):
    output = []
    probabilita_uno = [1 - bias, bias]

    for i in range(n_output):
        val = random.choices(list(range(2)), probabilita_uno)[0]
        output.append(val)

    return output


# Scrittore stati su file
def print_states(n_genes, n_cond, states, file_name):
    with open(file_name, "w") as file:
        file.write(f"n_genes: {n_genes} n_cond: {n_cond}\n")

        for row in states:
            for x in row:
                file.write(f"{x} ")
            file.write("\n")