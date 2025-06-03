from utils import read_file, print_states


# Lettore RBN
def read_graph(file_name):
    graph = {}

    with open(file_name, "r", encoding="utf-8") as file:
        lines = file.readlines()

    n_genes = lines[0].split(":")[1].strip()

    # Leggo il file une gene (3 righe) alla volta
    for g in range(1, len(lines), 3):
        gene = lines[g].split(":")[1].strip()
        ingressi_app = lines[g + 1].split(":")[1].strip()
        uscite_app = lines[g + 2].split(":")[1].strip()

        ingressi = [int(x) for x in ingressi_app.split()]
        uscite = [int(x) for x in uscite_app.split()]

        nodo = {"ingressi": ingressi, "uscite": uscite}

        graph[gene] = nodo

    return n_genes, graph


# Lettore condizioni iniziali
def generate_initconditions(file_name):
    init_conditions = {}

    with open(file_name, "r", encoding="utf-8") as file:
        first_line = file.readline().split()

        n_genes = int(first_line[1])
        n_cond = int(first_line[3])

        for c in range(n_cond):
            init_condition = [int(x) for x in file.readline().split()]
            init_conditions[c] = init_condition

    return n_cond, init_conditions


def simulate_steps(n_steps, graph, init_condition):
    state = init_condition

    for s in range(n_steps):
        new_state = []

        # Scorro tutti i nodi della rete
        for n_gene, data_gene in graph.items():
            ingressi = data_gene["ingressi"]
            uscite = data_gene["uscite"]

            # Recupero i valori degli ingressi dallo stato procedente -> Ricavo l'output a partire dagli ingressi intesi come numero binario
            input_values = [state[i] for i in ingressi] # Valori degli ingressi presi dallo stato precedente
            str_index = ''.join(map(str, input_values)) # Indice binario come stringa per accedere all'output
            index = int(str_index, 2) # Indice binario come stringa trasformato in indice decimale intero intero
            new_state.append(uscite[index])

        state = new_state

    return state


if __name__ == "__main__":

    # Lettura parametri
    input_file = "input_motore.txt"
    parameters = read_file(input_file)

    n_steps = int(parameters["n_steps"])

    # Lettura RBN
    n_genes, graph = read_graph("grafo_default.txt")

    # Lettura condizioni iniziali
    n_cond, init_conditions = generate_initconditions("cond_default.txt")

    final_states = []
    for c in range(n_cond):
        final_state = simulate_steps(n_steps, graph, init_conditions[c])
        final_states.append(final_state)

    print_states(n_genes, n_cond, final_states, "output_motore.txt")