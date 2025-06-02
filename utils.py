import random


def read_file(file_name):
    parameters_app = {}

    with open(file_name, "r", encoding="utf-8") as file:
        for line in file:
            if ":" in line:
                parameters_app[line.split(":")[0].strip()] = line.split(":")[1].strip()

    return parameters_app

def generate_random_boolean_output(n_uscite, bias):
    uscite = []
    probabilita_uscita = [1 - bias, bias]

    for u in range(n_uscite):
        uscita = random.choices(list(range(2)), probabilita_uscita)[0]
        uscite.append(uscita)

    return uscite

def print_states(n_genes, n_cond, states, file_name):
    with open(file_name, "w") as file:
        file.write(f"n_genes: {n_genes} n_cond: {n_cond}\n")

        for row in states:
            for x in row:
                file.write(f"{x} ")
            file.write("\n")