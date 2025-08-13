import os
from decimal import Decimal, getcontext


# Lettore parametri da file
def read_file(file_name):
    parameters_app = {}

    with open(file_name, "r", encoding="utf-8") as file:
        next_read = ""

        for line in file:
            if ":" in line:
                next_read = ""
                parameters_app[line.split(":")[0].strip()] = line.split(":")[1].strip()
            elif "ESSENZIALI" in line:
                next_read = "essenziali"
                parameters_app["essenziali"] = {}

            if next_read == "essenziali":
                parts = line.split()
                if len(parts) == 2:
                    nodo = int(parts[0])
                    val = Decimal(parts[1])
                    parameters_app["essenziali"][nodo] = val

    return parameters_app


# Lettore stati
def read_states(file_name):
    states = {}

    with open(file_name, "r", encoding="utf-8") as file:
        first_line = file.readline().split()
        # second_line = file.readline().split() # init_condition

        n_cond = int(first_line[3])

        for index, line in enumerate(file):
            state = [int(x) for x in line.split()]
            states[index] = state

    return n_cond, states


# Controllore ammissibilità parametri
def check_parameters(n_cond, n_states):
    # Il numero di stati deve essere un multiplo del numero delle condizioni iniziali, altrimenti non posso dividere in parti uguali l'elenco degli stati
    if (n_states % n_cond) != 0:
        raise ValueError("Numero degli stati non corrisponde al numero di condizioni iniziali")


# Divide l'elenco di stati in liste, dove una lista rappresenta l'evoluzione di una condizione iniziale
def split_list(c, n_states_condition, states):
    new_states = {}

    for i in range(c * int(n_states_condition), (c + 1) * int(n_states_condition)):
        new_states[i] = states[i]

    return new_states


# Calcola il benessere dell'agente
def calculate_benessere(states, omega, essenziali):

    # Variabile temporanea per calcolare la media dei valori dei nodi essenziali
    agent_node_val_sum = {Decimal(str(x)): 0 for x in essenziali}

    # Somma distanze euclidee
    distance_sum = Decimal('0')

    distance_steps = Decimal('0')
    c_step = Decimal('0')

    for i, s in enumerate(states):
        # Sommo i valori dei nodi essenziali
        for e in essenziali:
            agent_node_val_sum[e] += states[s][e]

        if (i + Decimal('1')) % omega == 0:
            for e in essenziali:
                agent_node_val_med = agent_node_val_sum[e] / omega
                #print(str(e) + ": " + str(agent_node_val_med))

                distance_sum += pow((agent_node_val_med - essenziali[e]), 2)
                #print(str(e) + ": " + str(pow((agent_node_val_med - essenziali[e]), 2)))

            distance_steps += distance_sum.sqrt()
            #print(round(distance_sum.sqrt(), 6))
            c_step += 1

            agent_node_val_sum = {x: 0 for x in agent_node_val_sum}
            distance_sum = 0
            #print("\n")

    benessere = distance_steps / c_step

    return benessere


# Scrittura benessere su file
def print_benessere(file_name, benessere_list):
    with open(file_name, "w") as file:
        for benessere in benessere_list:
            file.write(f"{benessere:.10f}\n")


def main():
    # Imposta la precisione a 28 cifre decimali
    getcontext().prec = 28

    parameters = read_file("input_benessere.txt")

    omega = Decimal(parameters["omega"])
    # ID NODO AGENTE - Valore ideale
    essenziali = parameters["essenziali"]

    n_cond, states = read_states(os.path.join("agent", "output_interaction_mode3.txt"))

    check_parameters(n_cond, len(states))
    n_states_condition = len(states) / n_cond

    benessere_list = []

    for c in range(n_cond):
        states_condition = split_list(c, n_states_condition, states)

        benessere = round(calculate_benessere(states_condition, omega, essenziali), 10)
        benessere_list.append(benessere)
        print(f"Benessere: {benessere:.10f}")

    print_benessere("benessere_agent.txt", benessere_list)


if __name__ == "__main__":
    main()