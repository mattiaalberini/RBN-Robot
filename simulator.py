import os

from utils import read_file, print_states, read_initconditions, read_graph, simulate_step, get_args


# Motore RBN mode 1
def simulate_steps_mode1(n_steps, graph, init_condition):
    state = init_condition

    for s in range(n_steps - 1):
        new_state = simulate_step(state, graph)
        state = new_state

    return state


# Motore RBN mode 2
def simulate_steps_mode2(n_steps, graph, init_condition):
    state = init_condition

    # Lista degli stati passo per passo
    states = []

    for s in range(n_steps - 1):
        new_state = simulate_step(state, graph)
        state = new_state
        states.append(state)

    return states


# Motore RBN mode 3
def simulate_steps_mode3(n_steps, graph, init_condition, finmax):
    state = init_condition

    # Lista degli stati passo per passo
    states = [state]

    for s in range(n_steps - 1):
        # Se il numero di stati in memoria è grande come finmax, rimuovo il primo elemento
        if len(states) == finmax:
            state.pop(0)

        new_state = simulate_step(state, graph)
        state = new_state

        if state in states:
            periodo = len(states) - states.index(state) # Numero di stati che si ripetono
            steps_attrattore = len(states) - periodo # Numero di passi fatti per trovare l'attrattore

            lista_attrattore = []

            for i in range(periodo):
                lista_attrattore.append(states[steps_attrattore + i])

            attrattore = max(lista_attrattore)

            return attrattore, periodo, steps_attrattore

        else:
            states.append(state)

    return -1, -1, -1


# Stampa mode 3
def print_mode3(list_attrattore, list_periodo, list_steps_attrattore, n_genes, n_cond, file_name):
    with open(file_name, "w") as file:
        file.write(f"n_genes: {n_genes} n_cond: {n_cond}\n")

        for c in range(n_cond):
            for a in list_attrattore[c]:
                file.write(f"{a} ")
            file.write(f"  {list_periodo[c]} {list_steps_attrattore[c]}\n")


def simulate_entity(directory):
    # Lettura parametri
    parameters = read_file(os.path.join(directory, "input_motore.txt"))

    n_steps = int(parameters["n_steps"])
    mode = int(parameters["mode"])

    # Lettura RBN
    n_genes, graph = read_graph(os.path.join(directory, "grafo_default.txt"))

    # Lettura condizioni iniziali
    n_cond, init_conditions = read_initconditions(os.path.join(directory, "cond_default.txt"))

    final_states = []

    output_file = os.path.join(directory, "output_motore.txt")

    # Mode 1: stampo solo lo stato finale
    if mode == 1:
        for c in range(n_cond):
            final_state = simulate_steps_mode1(n_steps, graph, init_conditions[c])
            final_states.append(final_state)

        print_states(n_genes, n_cond, final_states, output_file)

    # Mode 2: stampo tutti gli stati passo per passo
    elif mode == 2:
        for c in range(n_cond):
            final_states.append(init_conditions[c])
            states = simulate_steps_mode2(n_steps, graph, init_conditions[c])
            # Scorro la lista con tutti i passi e metto gli stati nella lista da stampare
            for s in states:
                final_states.append(s)

        print_states(n_genes, n_cond, final_states, output_file)

    # Mode 3: ricerca attrattori
    elif mode == 3:
        list_attrattore = []
        list_periodo = []
        list_steps_attrattore = []

        for c in range(n_cond):
            finmax = int(parameters["finmax"])
            attrattore, periodo, steps_attrattore = simulate_steps_mode3(n_steps, graph, init_conditions[c], finmax)

            list_attrattore.append(attrattore)
            list_periodo.append(periodo)
            list_steps_attrattore.append(steps_attrattore)

        print_mode3(list_attrattore, list_periodo, list_steps_attrattore, n_genes, n_cond, output_file)


def main():
    args = get_args()

    if args.agent:
        simulate_entity("agent")
        print("Avvenuta simulazione agente")
    if args.env:
        simulate_entity("environment")
        print("Avvenuta simulazione ambiente")
    if not args.agent and not args.env:
        print("Nessun parametro fornito. Usa -a e/o -e per simulare RBN.")


if __name__ == "__main__":
    main()