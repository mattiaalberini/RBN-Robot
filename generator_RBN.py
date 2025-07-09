import random
import os

import utils
from utils import read_file, generate_random_boolean_values, get_args


# Controllore ammissibilità parametri
def check_parameters(n_nodi, k_minimo, k_massimo, probabilita_k, bias_per_ogni_k):
    if n_nodi < 0:
        raise ValueError("Numero nodi negativo")

    if n_nodi - k_massimo < 1:
        raise ValueError("Numero k input elevato rispetto al numero nodi")

    if (k_massimo - k_minimo + 1) != len(probabilita_k):
        raise ValueError("Numero probabilita_k diverso dal numero di valori possibili di k")

    if (k_massimo - k_minimo + 1) != len(bias_per_ogni_k):
        raise ValueError("Numero bias_per_ogni_k diverso dal numero di valori possibili di k")

    if sum(probabilita_k) != 1:
        raise ValueError("Somma probabilita_k diversa da 1")

    if any(b < 0 or b > 1 for b in bias_per_ogni_k):
        raise ValueError("Valore bias_per_ogni_k non compreso tra 0 e 1")


# Generatore RBN
def generate_graph(n_nodi, k_minimo, k_massimo, probabilita_k, bias_per_ogni_k):
    graph = {}

    for n in range(n_nodi):
        # Numero ingressi per nodo
        n_ingressi = random.choices(list(range(k_minimo, k_massimo + 1)), probabilita_k)[0]

        ingressi = []
        for i in range(n_ingressi):
            # Generazione ingressi evitando duplicati
            ingresso = random.choice([x for x in range(n_nodi) if x not in ingressi and x != n])
            ingressi.append(ingresso)

        # Numero uscite per nodo
        n_uscite = pow(2, n_ingressi)

        # Bias a seconda del numero di ingressi (k)
        bias = bias_per_ogni_k[n_ingressi - k_minimo]

        uscite = generate_random_boolean_values(n_uscite, bias)

        nodo = {"ingressi": ingressi, "uscite": uscite}
        graph[n] = nodo

    return graph


# Scrittore RBN su file
def print_grafo(n_nodi, graph, directory):
    with open(os.path.join(directory, "grafo_default.txt"), "w") as file:
        file.write(f"n_genes: {n_nodi}\n")

        for n in range(n_nodi):
            file.write(f"gene: {n}\n")

            # Ingressi
            file.write(f"lista ingressi ({len(graph[n]["ingressi"])}):")
            for i in graph[n]["ingressi"]:
                file.write(f" {i}")
            file.write("\n")

            # Uscite
            file.write(f"uscite ({len(graph[n]["uscite"])}):")
            for u in graph[n]["uscite"]:
                file.write(f" {u}")
            file.write("\n")


def generate_component(directory):
    input_file = os.path.join(directory, "input_generatore.txt")

    parameters = read_file(input_file)

    # Conversione parametri
    n_nodi = int(parameters["n_nodi"])
    seme = int(parameters["seme"])
    k_minimo = int(parameters["k_minimo"])
    k_massimo = int(parameters["k_massimo"])
    probabilita_k = list(map(float, parameters["probabilità_k"].split()))
    bias_per_ogni_k = list(map(float, parameters["bias_per_ogni_k"].split()))

    # Controllo parametri
    check_parameters(n_nodi, k_minimo, k_massimo, probabilita_k, bias_per_ogni_k)

    # Imposto il seed
    if seme != 0:
        random.seed(seme)

    # Generazione grafo
    graph = generate_graph(n_nodi, k_minimo, k_massimo, probabilita_k, bias_per_ogni_k)

    # Scrivo grafo su file
    print_grafo(n_nodi, graph, directory)


def main():
    args = get_args()

    if args.agent:
        generate_component("agent")
        print("Agente generato")
    if args.env:
        generate_component("environment")
        print("Ambiente generato")
    if not args.agent and not args.env:
        print("Nessun parametro fornito. Usa -a e/o -e per generare RBN.")


if __name__ == "__main__":
    main()