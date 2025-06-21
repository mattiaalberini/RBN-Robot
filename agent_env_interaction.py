import os

from utils import read_graph, read_initconditions, print_states, simulate_step


# Controllore ammissibilità parametri
def check_parameters(agent_ncond, env_ncond):
    # Agente e ambiente devono avere lo stesso numero di condizioni iniziali
    if agent_ncond != env_ncond:
        raise ValueError("Numero condizioni iniziali agente e ambiente diverso")


def simulate_agent_env_steps(agent_rbn, env_rbn, tot_steps, agent_step, env_step, soglia_sensori, soglia_effettori, effettori, sensori, agent_state, env_state, agent_node_val_sum, env_node_val_sum):
    agent_states, env_states = [], []
    agent_states.append(list(agent_state))
    env_states.append(list(env_state))

    # Inizializzo a 0
    agent_node_val_sum = {x: 0 for x in agent_node_val_sum}
    env_node_val_sum = {x: 0 for x in env_node_val_sum}

    for s in range(1, tot_steps):
        print(s)
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
                    agent_rbn[sensori[e]]["uscite"] = [0 for _ in agent_rbn[sensori[e]]["uscite"]]
                    agent_state[sensori[e]] = 0
                    print("Nodo " + str(sensori[e]) + " -> 0 (preso da nodo " + str(e) + " dell'ambiente)")
                else:
                    # Media < Soglia -> Le uscite del nodo saranno tutte 1 e il nodo sarà = 1
                    agent_rbn[sensori[e]]["uscite"] = [1 for _ in agent_rbn[sensori[e]]["uscite"]]
                    agent_state[sensori[e]] = 1
                    print("Nodo " + str(sensori[e]) + " -> 1 (preso da nodo " + str(e) + " dell'ambiente)")

            agent_state = simulate_step(agent_state, agent_rbn)

            env_node_val_sum = {x: 0 for x in env_node_val_sum}

        if s % env_step == 0:
            # L'agente modifica l'ambiente
            print("Modifica ambiente")
            for e in agent_node_val_sum:
                if agent_node_val_sum[e] / env_step < soglia_effettori:
                    # Media < Soglia -> Le uscite del nodo saranno tutte 0 e il nodo sarà = 0
                    env_rbn[effettori[e]]["uscite"] = [0 for _ in env_rbn[effettori[e]]["uscite"]]
                    env_state[effettori[e]] = 0
                    print("Nodo " + str(effettori[e]) + " -> 0 (preso da nodo " + str(e) + " dell'agente)")
                else:
                    # Media < Soglia -> Le uscite del nodo saranno tutte 1 e il nodo sarà = 1
                    env_rbn[effettori[e]]["uscite"] = [1 for _ in env_rbn[effettori[e]]["uscite"]]
                    env_state[effettori[e]] = 1
                    print("Nodo " + str(effettori[e]) + " -> 1 (preso da nodo " + str(e) + " dell'agente)")

            env_state = simulate_step(env_state, env_rbn)

            agent_node_val_sum = {x: 0 for x in agent_node_val_sum}

        agent_states.append(list(agent_state))
        env_states.append(list(env_state))
        print("\n")

    return agent_states, env_states



def main():
    agent_num_genes, agent_rbn = read_graph(os.path.join("agent", "grafo_default.txt"))
    env_num_genes, env_rbn = read_graph(os.path.join("environment", "grafo_default.txt"))

    agent_ncond, agent_initconditions = read_initconditions(os.path.join("agent", "cond_default.txt"))
    env_ncond, env_initconditions = read_initconditions(os.path.join("environment", "cond_default.txt"))

    tot_steps = 20
    agent_step = 3
    env_step = 5

    soglia_sensori = 0.9 # Ambiente che modifica l'agente
    soglia_effettori = 0.9 # Agente che modifica l'ambiente

    # ID NODO AGENTE - ID NODO AMBIENTE
    effettori = {
        2: 14,
        13: 3
    }

    # Ho invertito l'ordine rispetto al file
    # ID NODO AMBIENTE - ID NODO AGENTE
    sensori = {
        15: 12,
        0: 1,
        12: 2
    }

    # Controllo la correttezza dei parametri
    check_parameters(agent_ncond, env_ncond)

    # Variabile temporanea per calcolare la media dei valori che interagiscono con l'altra RBN
    agent_node_val_sum = {x: 0 for x in effettori}
    env_node_val_sum = {x: 0 for x in sensori}

    agent_states, env_states = [], []

    for c in range(agent_ncond):

        agent_state = agent_initconditions[c]
        env_state = env_initconditions[c]

        agent_states, env_states = simulate_agent_env_steps(agent_rbn, env_rbn, tot_steps, agent_step, env_step, soglia_sensori, soglia_effettori, effettori, sensori, agent_state, env_state, agent_node_val_sum, env_node_val_sum)

    print_states(agent_num_genes, agent_ncond, agent_states, os.path.join("agent", "output_interaction.txt"))
    print_states(env_num_genes, env_ncond, env_states, os.path.join("environment", "output_interaction.txt"))


if __name__ == "__main__":
    main()