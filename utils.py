import random


# Lettore parametri da file
def read_file(file_name):
    parameters_app = {}

    with open(file_name, "r", encoding="utf-8") as file:
        for line in file:
            if ":" in line:
                parameters_app[line.split(":")[0].strip()] = line.split(":")[1].strip()

    return parameters_app


# Lettore RBN
def read_graph(file_name):
    graph = {}

    with open(file_name, "r", encoding="utf-8") as file:
        lines = file.readlines()

    n_genes = lines[0].split(":")[1].strip()

    # Leggo il file une gene (3 righe) alla volta
    for g in range(1, len(lines), 3):
        gene = int(lines[g].split(":")[1].strip())
        ingressi_app = lines[g + 1].split(":")[1].strip()
        uscite_app = lines[g + 2].split(":")[1].strip()

        ingressi = [int(x) for x in ingressi_app.split()]
        uscite = [int(x) for x in uscite_app.split()]

        nodo = {"ingressi": ingressi, "uscite": uscite}

        graph[gene] = nodo

    return n_genes, graph


# Lettore condizioni iniziali
def read_initconditions(file_name):
    init_conditions = {}

    with open(file_name, "r", encoding="utf-8") as file:
        first_line = file.readline().split()

        n_genes = int(first_line[1])
        n_cond = int(first_line[3])

        for c in range(n_cond):
            init_condition = [int(x) for x in file.readline().split()]
            init_conditions[c] = init_condition

    return n_cond, init_conditions


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


# Scelta del file dove prendere i dati in input (agente o ambiente)
def input_choice(testo):
    print("Scegliere cosa " + testo + ":")
    print("1. Agente")
    print("2. Ambiente")

    valid_choice = False
    directory = ""

    while not valid_choice:
        choice = input("Inserire 1 o 2: ")

        if choice == "1":
            directory = "agent"
            valid_choice = True
        elif choice == "2":
            directory = "environment"
            valid_choice = True
        else:
            print("Scelta non valida. Riprovare inserendo 1 o 2.")

    return directory


def simulate_step(state, graph):
    new_state = []

    # Scorro tutti i nodi della rete
    for n_gene, data_gene in graph.items():
        ingressi = data_gene["ingressi"]
        uscite = data_gene["uscite"]

        # Recupero i valori degli ingressi dallo stato procedente -> Ricavo l'output a partire dagli ingressi intesi come numero binario -> Nuovo stato
        input_values = [state[i] for i in ingressi]  # Valori degli ingressi presi dallo stato precedente
        str_index = ''.join(map(str, input_values))  # Indice binario come stringa per accedere all'output
        index = int(str_index, 2)  # Indice binario come stringa trasformato in indice decimale intero intero

        new_state.append(uscite[index])

    return new_state