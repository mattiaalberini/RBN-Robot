import os

from utils import read_file, print_states, input_choice, read_initconditions, read_graph, simulate_step


# Motore RBN mode 1
def simulate_steps_mode1(n_steps, graph, init_condition):
    state = init_condition

    for s in range(n_steps):
        new_state = simulate_step(state, graph)
        state = new_state

    return state


# Motore RBN mode 2
def simulate_steps_mode2(n_steps, graph, init_condition):
    state = init_condition

    # Lista degli stati passo per passo
    states = []

    for s in range(n_steps):
        new_state = simulate_step(state, graph)
        state = new_state
        states.append(state)

    return states


if __name__ == "__main__":

    # Scelta se lavorare con l'agente o con l'ambiente
    directory = input_choice("simulare")

    # Lettura parametri
    parameters = read_file(os.path.join(directory, "input_motore.txt"))

    n_steps = int(parameters["n_steps"])
    mode = int(parameters["mode"])

    # Lettura RBN
    n_genes, graph = read_graph(os.path.join(directory, "grafo_default.txt"))

    # Lettura condizioni iniziali
    n_cond, init_conditions = read_initconditions(os.path.join(directory, "cond_default.txt"))

    final_states = []

    # Mode 1: stampo solo lo stato finale
    if mode == 1:
        for c in range(n_cond):
            final_state = simulate_steps_mode1(n_steps, graph, init_conditions[c])
            final_states.append(final_state)

    # Mode 2: stampo tutti gli stati passo per passo
    elif mode == 2:
        for c in range(n_cond):
            states = simulate_steps_mode2(n_steps, graph, init_conditions[c])
            # Scorro la lista con tutti i passi e metto gli stati nella lista da stampare
            for s in states:
                final_states.append(s)

    output_file = os.path.join(directory, "output_motore.txt")
    print_states(n_genes, n_cond, final_states, output_file)