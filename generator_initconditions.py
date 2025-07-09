import random, os

import utils
from utils import read_file, generate_random_boolean_values, print_states, get_args


# Controllore ammissibilità parametri
def check_parameters(n_genes, n_cond, bias):
    if n_genes < 0:
        raise ValueError("Numero geni negativo")

    if n_cond < 0:
        raise ValueError("Numero condizioni negativo")

    if bias < 0 or bias > 1:
        raise ValueError("Valore bias non compreso tra 0 e 1")


# Generatore condizioni iniziali
def generate_initconditions(n_genes, n_cond, bias):
    init_conditions = []

    for c in range(n_cond):
        # Genero una condizione iniziale
        init_condition = generate_random_boolean_values(n_genes, bias)
        init_conditions.append(init_condition)

    return init_conditions


def generate_component(directory):
    # Lettura parametri
    input_file = os.path.join(directory, "input_gen_cond.txt")
    parameters = read_file(input_file)

    # Conversione parametri
    n_genes = int(parameters["n_genes"])
    n_cond = int(parameters["n_cond"])
    bias = float(parameters["bias"])
    seme = int(parameters["seme"])

    # Controllo parametri
    check_parameters(n_genes, n_cond, bias)

    # Imposto il seed
    if seme != 0:
        random.seed(seme)

    # Generazione condizioni iniziali
    initconditions = generate_initconditions(n_genes, n_cond, bias)

    # Scrittura condizioni iniziali su file
    output_file = os.path.join(directory, "cond_default.txt")
    print_states(n_genes, n_cond, initconditions, output_file)


def main():
    args = get_args()

    if args.agent:
        generate_component("agent")
        print("Condizioni iniziali agente generate")
    if args.env:
        generate_component("environment")
        print("Condizioni iniziali ambiente generate")
    if not args.agent and not args.env:
        print("Nessun parametro fornito. Usa -a e/o -e per generare le condizioni iniziali.")


if __name__ == "__main__":
    main()
