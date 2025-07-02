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


def calculate_benessere(states, omega, essenziali):

    # Variabile temporanea per calcolare la media dei valori dei nodi essenziali
    agent_node_val_sum = {Decimal(str(x)): 0 for x in essenziali}

    # Somma distanze euclidee
    distance_sum = Decimal('0')

    distance_steps = Decimal('0')
    c_step = Decimal('0')

    for s in states:
        # Sommo i valori dei nodi essenziali
        for e in essenziali:
            #print(s, e)
            agent_node_val_sum[e] += states[s][e]

        if (s + 1) % omega == 0:
            for e in essenziali:
                agent_node_val_med = agent_node_val_sum[e] / omega
                #print(str(e) + ": " + str(agent_node_val_med))

                distance_sum += pow((agent_node_val_med - essenziali[e]), 2)
                print(pow((agent_node_val_med - essenziali[e]), 2))

            distance_steps += distance_sum.sqrt()
            print(round(distance_sum.sqrt(), 6))
            c_step += 1


            agent_node_val_sum = {x: 0 for x in agent_node_val_sum}
            distance_sum = 0
            print("\n")

    benessere = distance_steps / c_step
    return benessere



def main():
    # Imposta la precisione a 28 cifre decimali
    getcontext().prec = 28

    parameters = read_file("input_benessere.txt")

    omega = Decimal(parameters["omega"])
    # ID NODO AGENTE - Valore ideale
    essenziali = parameters["essenziali"]

    n_cond, states = read_states(os.path.join("agent", "output_interaction_mode3.txt"))

    benessere = calculate_benessere(states, omega, essenziali)

    print(benessere)

if __name__ == "__main__":
    main()