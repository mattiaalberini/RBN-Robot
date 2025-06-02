import random

from utils import read_file, generate_random_boolean_output, print_states


def generate_initcondition(n_genes, n_cond, bias, seme):
    if seme != 0:
        random.seed(seme)

    init_conditions = []

    for c in range(n_cond):
        init_condition = generate_random_boolean_output(n_genes, bias)
        init_conditions.append(init_condition)

    return init_conditions

if __name__ == "__main__":

    # Lettura parametri
    input_file = "input_gen_cond.txt"
    parameters = read_file(input_file)

    # Conversione parametri
    n_genes = int(parameters["n_genes"])
    n_cond = int(parameters["n_cond"])
    bias = float(parameters["bias"])
    seme = int(parameters["seme"])

    initconditions = generate_initcondition(n_genes, n_cond, bias, seme)

    print_states(n_genes, n_cond, initconditions, "cond_default.txt")