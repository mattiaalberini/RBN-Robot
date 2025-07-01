import os

from utils import read_graph, read_initconditions, print_states, simulate_step


# Lettore parametri da file
def read_file(file_name):
    parameters_app = {}

    with open(file_name, "r", encoding="utf-8") as file:
        next_read = ""

        for line in file:
            if ":" in line:
                next_read = ""
                parameters_app[line.split(":")[0].strip()] = line.split(":")[1].strip()
            elif "EFFETTORI" in line:
                next_read = "effettori"
                parameters_app["effettori"] = {}
            elif "SENSORI" in line:
                next_read = "sensori"
                parameters_app["sensori"] = {}

            if next_read == "effettori":
                parts = line.split()
                if len(parts) == 2:
                    agent, env = map(int, parts)
                    parameters_app["effettori"][agent] = env
            elif next_read == "sensori":
                parts = line.split()
                if len(parts) == 2:
                    agent, env = map(int, parts)
                    parameters_app["sensori"][env] = agent


    return parameters_app


# Controllore ammissibilità parametri
def check_parameters(agent_ncond, env_ncond):
    # Agente e ambiente devono avere lo stesso numero di condizioni iniziali
    if agent_ncond != env_ncond:
        raise ValueError("Numero condizioni iniziali agente e ambiente diverso")


def simulate_agent_env_step (s, agent_rbn, env_rbn, agent_step, env_step, soglia_sensori, soglia_effettori, effettori, sensori, agent_state, env_state, agent_node_val_sum, env_node_val_sum, effettori_old_new_val, sensori_old_new_val):
    # Tengo traccia dei valori dei nodi effettori e dei nodi letti dai sensori
    # Nodi effettori
    for a in agent_node_val_sum:
        agent_node_val_sum[a] += agent_state[a]
    # Nodi letti dai sensori
    for e in env_node_val_sum:
        env_node_val_sum[e] += env_state[e]

    if s % agent_step == 0:
        # L'agente si modifica
        print("Modifica agente")
        for e in env_node_val_sum:
            if env_node_val_sum[e] / agent_step < soglia_sensori:
                # Media < Soglia -> Le uscite del nodo saranno tutte 0 e il nodo sarà = 0
                #agent_rbn[sensori[e]]["uscite"] = [0 for _ in agent_rbn[sensori[e]]["uscite"]]
                agent_state[sensori[e]] = 0
                print("Nodo " + str(sensori[e]) + " -> 0 (preso da nodo " + str(e) + " dell'ambiente)")
            else:
                # Media < Soglia -> Le uscite del nodo saranno tutte 1 e il nodo sarà = 1
                #agent_rbn[sensori[e]]["uscite"] = [1 for _ in agent_rbn[sensori[e]]["uscite"]]
                agent_state[sensori[e]] = 1
                print("Nodo " + str(sensori[e]) + " -> 1 (preso da nodo " + str(e) + " dell'ambiente)")

        agent_state = simulate_step(agent_state, agent_rbn)

        # Correggo il valore dei nodi sensori che sono stati modificati durante la simulazione
        for e in env_node_val_sum:
            if env_node_val_sum[e] / agent_step < soglia_sensori:
                # Media < Soglia -> Le uscite del nodo saranno tutte 0 e il nodo sarà = 0
                sensori_old_new_val[sensori[e]].append({"old": agent_state[sensori[e]], "new": 0})
                agent_state[sensori[e]] = 0
            else:
                # Media < Soglia -> Le uscite del nodo saranno tutte 1 e il nodo sarà = 1
                sensori_old_new_val[sensori[e]].append({"old": agent_state[sensori[e]], "new": 1})
                agent_state[sensori[e]] = 1

        env_node_val_sum = {x: 0 for x in env_node_val_sum}
    else:
        for e in env_node_val_sum:
            sensori_old_new_val[sensori[e]].append({"old": -1, "new": -1})


    if s % env_step == 0:
        # L'agente modifica l'ambiente
        print("Modifica ambiente")
        for e in agent_node_val_sum:
            if agent_node_val_sum[e] / env_step < soglia_effettori:
                # Media < Soglia -> Le uscite del nodo saranno tutte 0 e il nodo sarà = 0
                #env_rbn[effettori[e]]["uscite"] = [0 for _ in env_rbn[effettori[e]]["uscite"]]
                env_state[effettori[e]] = 0
                print("Nodo " + str(effettori[e]) + " -> 0 (preso da nodo " + str(e) + " dell'agente)")
            else:
                # Media < Soglia -> Le uscite del nodo saranno tutte 1 e il nodo sarà = 1
                #env_rbn[effettori[e]]["uscite"] = [1 for _ in env_rbn[effettori[e]]["uscite"]]

                env_state[effettori[e]] = 1
                print("Nodo " + str(effettori[e]) + " -> 1 (preso da nodo " + str(e) + " dell'agente)")

        env_state = simulate_step(env_state, env_rbn)

        # Correggo il valore dei nodi su cui hanno effetto gli effettori che sono stati modificati durante la simulazione
        for e in agent_node_val_sum:
            if agent_node_val_sum[e] / env_step < soglia_effettori:
                # Media < Soglia -> Le uscite del nodo saranno tutte 0 e il nodo sarà = 0
                effettori_old_new_val[effettori[e]].append({"old": env_state[effettori[e]], "new": 0})
                env_state[effettori[e]] = 0
            else:
                # Media < Soglia -> Le uscite del nodo saranno tutte 1 e il nodo sarà = 1
                effettori_old_new_val[effettori[e]].append({"old": env_state[effettori[e]], "new": 1})
                env_state[effettori[e]] = 1

        agent_node_val_sum = {x: 0 for x in agent_node_val_sum}
    else:
        for e in agent_node_val_sum:
            effettori_old_new_val[effettori[e]].append({"old": -1, "new": -1})


    return agent_state, env_state, agent_node_val_sum, env_node_val_sum


# Mode 1: solo stato finale
def simulate_agent_env_steps_mode1(agent_rbn, env_rbn, tot_steps, agent_step, env_step, soglia_sensori, soglia_effettori, effettori, sensori, agent_state, env_state, agent_node_val_sum, env_node_val_sum, effettori_old_new_val, sensori_old_new_val):

    # Variabile temporanea per calcolare la media dei valori che interagiscono con l'altra RBN
    agent_node_val_sum = {x: 0 for x in agent_node_val_sum}
    env_node_val_sum = {x: 0 for x in env_node_val_sum}

    for s in range(1, tot_steps):
        print(s)
        agent_state, env_state, agent_node_val_sum, env_node_val_sum = simulate_agent_env_step(s, agent_rbn, env_rbn, agent_step, env_step, soglia_sensori, soglia_effettori, effettori, sensori, agent_state, env_state, agent_node_val_sum, env_node_val_sum, effettori_old_new_val, sensori_old_new_val)
        print("\n")

    return agent_state, env_state


# Mode 2: tutti gli stati
def simulate_agent_env_steps_mode2(agent_rbn, env_rbn, tot_steps, agent_step, env_step, soglia_sensori, soglia_effettori, effettori, sensori, agent_state, env_state, agent_node_val_sum, env_node_val_sum, effettori_old_new_val, sensori_old_new_val):
    agent_states, env_states = [], []
    agent_states.append(list(agent_state))
    env_states.append(list(env_state))

    # Variabile temporanea per calcolare la media dei valori che interagiscono con l'altra RBN
    agent_node_val_sum = {x: 0 for x in agent_node_val_sum}
    env_node_val_sum = {x: 0 for x in env_node_val_sum}

    for s in range(1, tot_steps):
        print(s)
        agent_state, env_state, agent_node_val_sum, env_node_val_sum = simulate_agent_env_step(s, agent_rbn, env_rbn, agent_step, env_step, soglia_sensori, soglia_effettori, effettori, sensori, agent_state, env_state, agent_node_val_sum, env_node_val_sum, effettori_old_new_val, sensori_old_new_val)
        agent_states.append(list(agent_state))
        env_states.append(list(env_state))
        print("\n")

    return agent_states, env_states


# Mode 3: ogni stato al cambiamento
def simulate_agent_env_steps_mode3(agent_rbn, env_rbn, tot_steps, agent_step, env_step, soglia_sensori, soglia_effettori, effettori, sensori, agent_state, env_state, agent_node_val_sum, env_node_val_sum, effettori_old_new_val, sensori_old_new_val):
    agent_states, env_states = [], []
    agent_states.append(list(agent_state))
    env_states.append(list(env_state))

    # Variabile temporanea per calcolare la media dei valori che interagiscono con l'altra RBN
    agent_node_val_sum = {x: 0 for x in agent_node_val_sum}
    env_node_val_sum = {x: 0 for x in env_node_val_sum}

    for s in range(1, tot_steps):
        print(s)
        agent_state, env_state, agent_node_val_sum, env_node_val_sum = simulate_agent_env_step(s, agent_rbn, env_rbn, agent_step, env_step, soglia_sensori, soglia_effettori, effettori, sensori, agent_state, env_state, agent_node_val_sum, env_node_val_sum, effettori_old_new_val, sensori_old_new_val)

        if s % agent_step == 0:
            agent_states.append(list(agent_state))

        if s % env_step == 0:
            env_states.append(list(env_state))

        print("\n")

    return agent_states, env_states


def print_old_new_val(old_new_val, file_name):

    with open(file_name, 'w') as f:
        nodes = list(sorted(old_new_val.keys()))

        # Stampo due volte le chiavi
        f.write(' '.join(str(k) for k in nodes) + ' ')
        f.write(' '.join(str(k) for k in nodes) + '\n')

        # Numero massimo di righe
        num_righe = max(len(old_new_val[k]) for k in nodes)

        for i in range(num_righe):
            riga = []

            # Copia valori new
            for k in nodes:
                if i < len(old_new_val[k]):
                    val = old_new_val[k][i]['new']
                    riga.append(str(val) if val != -1 else ' ')
                else:
                    riga.append(' ')

            # Copia valori old
            for k in nodes:
                if i < len(old_new_val[k]):
                    val = old_new_val[k][i]['old']
                    riga.append(str(val) if val != -1 else ' ')
                else:
                    riga.append(' ')

            f.write(' '.join(riga) + '\n')


def main():

    parameters = read_file("input_AG_AMB.txt")
    print(parameters)

    agent_num_genes, agent_rbn = read_graph(os.path.join("agent", "grafo_default.txt"))
    env_num_genes, env_rbn = read_graph(os.path.join("environment", "grafo_default.txt"))

    agent_ncond, agent_initconditions = read_initconditions(os.path.join("agent", "cond_default.txt"))
    env_ncond, env_initconditions = read_initconditions(os.path.join("environment", "cond_default.txt"))

    tot_steps = int(parameters["n_steps"])
    agent_step = int(parameters["orologio agente"])
    env_step = int(parameters["orologio ambiente"])

    soglia_sensori = float(parameters["soglia sensori"]) # Ambiente che modifica l'agente
    soglia_effettori = float(parameters["soglia effettori"]) # Agente che modifica l'ambiente

    # ID NODO AGENTE - ID NODO AMBIENTE
    effettori = parameters["effettori"]
    # ID NODO AMBIENTE - ID NODO AGENTE
    sensori = parameters["sensori"]

    # Mode
    mode = int(parameters["mode"])

    # Controllo la correttezza dei parametri
    check_parameters(agent_ncond, env_ncond)

    # Variabile temporanea per calcolare la media dei valori che interagiscono con l'altra RBN
    agent_node_val_sum = {x: 0 for x in effettori}
    env_node_val_sum = {x: 0 for x in sensori}

    # Per confrontare i valori ottenuto dalla simulazione standard e i valori dell'interazione
    effettori_old_new_val = {v: [] for k, v in effettori.items()}
    sensori_old_new_val = {v: [] for k, v in sensori.items()}

    agent_final_states, env_final_states = [], []

    output_filename = "output_interaction.txt"

    # Mode 1: stampo solo stato finale
    if mode == 1:
        output_filename = "output_interaction_mode1.txt"

        for c in range(agent_ncond):
            for x in effettori:
                effettori_old_new_val[effettori[x]].append({"old": -1, "new": -1})
            for x in sensori:
                sensori_old_new_val[sensori[x]].append({"old": -1, "new": -1})

            agent_final_state, env_final_state = simulate_agent_env_steps_mode1(agent_rbn, env_rbn, tot_steps, agent_step, env_step, soglia_sensori, soglia_effettori, effettori, sensori, agent_initconditions[c], env_initconditions[c], agent_node_val_sum, env_node_val_sum, effettori_old_new_val, sensori_old_new_val)

            print(agent_final_state)
            print(env_final_state)

            agent_final_states.append(agent_final_state)
            env_final_states.append(env_final_state)

    # Mode 2: stampo tutti gli stati
    elif mode == 2:
        output_filename = "output_interaction_mode2.txt"

        for c in range(agent_ncond):
            for x in effettori:
                effettori_old_new_val[effettori[x]].append({"old": -1, "new": -1})
            for x in sensori:
                sensori_old_new_val[sensori[x]].append({"old": -1, "new": -1})

            agent_states, env_states = simulate_agent_env_steps_mode2(agent_rbn, env_rbn, tot_steps, agent_step, env_step, soglia_sensori, soglia_effettori, effettori, sensori, agent_initconditions[c], env_initconditions[c], agent_node_val_sum, env_node_val_sum, effettori_old_new_val, sensori_old_new_val)

            for a in agent_states:
                agent_final_states.append(a)
            for e in env_states:
                env_final_states.append(e)

    # Mode 3: stampo ogni stato al cambiamento
    elif mode == 3:
        output_filename = "output_interaction_mode3.txt"

        for c in range(agent_ncond):
            for x in effettori:
                effettori_old_new_val[effettori[x]].append({"old": -1, "new": -1})
            for x in sensori:
                sensori_old_new_val[sensori[x]].append({"old": -1, "new": -1})

            agent_states, env_states = simulate_agent_env_steps_mode3(agent_rbn, env_rbn, tot_steps, agent_step, env_step, soglia_sensori, soglia_effettori, effettori, sensori, agent_initconditions[c], env_initconditions[c], agent_node_val_sum, env_node_val_sum, effettori_old_new_val, sensori_old_new_val)

            for a in agent_states:
                agent_final_states.append(a)
            for e in env_states:
                env_final_states.append(e)


    print_states(agent_num_genes, agent_ncond, agent_final_states, os.path.join("agent", output_filename))
    print_states(env_num_genes, env_ncond, env_final_states, os.path.join("environment", output_filename))

    print_old_new_val(sensori_old_new_val, os.path.join("agent", "variazione_nodi.txt"))
    print_old_new_val(effettori_old_new_val, os.path.join("environment", "variazione_nodi.txt"))


if __name__ == "__main__":
    main()