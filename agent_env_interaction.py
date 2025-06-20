import os

from obj.RBN import RBN
from obj.RBNGene import RBNGene
from utils import read_initconditions


# Lettore RBN
def load_graph(file_name):
    graph = RBN()

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

        nodo = RBNGene(gene, ingressi, uscite)
        graph.add_gene(nodo)

    return graph


# Controllore ammissibilità parametri
def check_parameters(agent_ncond, env_ncond):
    # Agente e ambiente devono avere lo stesso numero di condizioni iniziali
    if agent_ncond != env_ncond:
        raise ValueError("Numero condizioni iniziali agente e ambiente diverso")



def main():
    agent_rbn = load_graph(os.path.join("agent", "grafo_default.txt"))
    env_rbn = load_graph(os.path.join("environment", "grafo_default.txt"))

    agent_ncond, agent_initconditions = read_initconditions(os.path.join("agent", "cond_default.txt"))
    env_ncond, env_initconditions = read_initconditions(os.path.join("environment", "cond_default.txt"))

    tot_steps = 20
    agent_step = 3
    env_step = 5

    soglia_sensori = 0.5 # Ambiente che modifica l'agente
    soglia_effettori = 0.4 # Agente che modifica l'ambiente

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

    # Variabile temporanea per calcolare la media dei valori che interagiscono con l'altra RBN
    agent_node_val_sum = {x: 0 for x in effettori}
    env_node_val_sum = {x: 0 for x in sensori}

    #Controllo la correttezza dei parametri
    check_parameters(agent_ncond, env_ncond)


    for c in range(agent_ncond):
        agent_rbn.set_initconditions(agent_initconditions[c])
        env_rbn.set_initconditions(env_initconditions[c])

        # Inizializzo a 0
        agent_node_val_sum = {x: 0 for x in agent_node_val_sum}
        env_node_val_sum = {x: 0 for x in env_node_val_sum}

        for s in range(1, tot_steps + 1):
            print(s)

            for a in agent_node_val_sum:
                agent_node_val_sum[a] += agent_rbn.get_gene_stato(a)
            for e in env_node_val_sum:
                env_node_val_sum[e] += env_rbn.get_gene_stato(e)


            if s % agent_step == 0:
                # L'agente si modifica
                print("Modifica agente")
                for e in env_node_val_sum:
                    if env_node_val_sum[e] / agent_step < soglia_sensori:
                        agent_rbn.set_gene_stato(e, 0)
                        print("Nodo " + str(sensori[e]) + " -> 0 (preso da nodo " + str(e) + " dell'ambiente)" )
                    else:
                        agent_rbn.set_gene_stato(e, 1)
                        print("Nodo " + str(sensori[e]) + " -> 1 (preso da nodo " + str(e) + " dell'ambiente)" )

                env_node_val_sum = {x: 0 for x in env_node_val_sum}


            if s % env_step == 0:
                # L'agente modifica l'ambiente
                print("Modifica ambiente")
                for e in agent_node_val_sum:
                    if agent_node_val_sum[e] / env_step < soglia_effettori:
                        env_rbn.set_gene_stato(e, 0)
                        print("Nodo " + str(effettori[e]) + " -> 0 (preso da nodo " + str(e) + " dell'agente)" )
                    else:
                        env_rbn.set_gene_stato(e, 1)
                        print("Nodo " + str(effettori[e]) + " -> 1 (preso da nodo " + str(e) + " dell'agente)" )

                agent_node_val_sum = {x: 0 for x in agent_node_val_sum}

            print("\n")

"""
            if s % env_step == 0:
                # L'agente modifica l'ambiente
                print("modifica ambiente")
                for e in env_node_val_sum:
                    if env_node_val_sum[e] / env_step < soglia_sensori:
                        agent_rbn.set_gene_stato(e, 0)
                    else:
                        agent_rbn.set_gene_stato(e, 1)
                    env_node_val_sum = {x: 0 for x in env_node_val_sum}
"""


if __name__ == "__main__":
    main()