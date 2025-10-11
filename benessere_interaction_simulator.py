import argparse
import copy
import os
import subprocess
import math

from generator_RBN import print_grafo
from utils import print_states, read_file, read_graph, generate_random_boolean_values


def check_parameters(n_iterazioni, mode):
    if n_iterazioni < 1:
        raise ValueError("Valore numero iterazioni non accettabile!")
    if mode != 'a' and mode != 'b':
        raise ValueError("Valore mode diverso da 'a' e 'b'!")


def read_init_condition(file_name):
    init_conditions = []
    periodo = 0

    with open(file_name, "r") as f:
        first_line = f.readline().strip()
        parts = first_line.split()
        for line in f:
            if line != "\n":
                if periodo == 0:
                    init_condition = [int(x) for x in line.strip().split()]
                    init_conditions.append(init_condition)
                periodo += 1
            else:
                return int(parts[1]), periodo, init_conditions

    return int(parts[1]), 0, None


def read_valori_ideali(file_name):
    valori_ideali = []

    with open(file_name, "r") as f:
        first_line = f.readline().strip()
        for line in f:
            if line != "\n":
                valori_ideali = [float(x) for x in line.strip().split()]
                break

    return valori_ideali


def read_nodi_effettori(file_name):
    effettori = []

    with open(file_name, "r", encoding="utf-8") as file:
        next_read = ""

        for line in file:
            if ":" in line or "SENSORI" in line:
                next_read = ""
            elif "EFFETTORI" in line:
                next_read = "effettori"

            if next_read == "effettori":
                parts = line.split()
                if len(parts) == 2:
                    agent, env = map(int, parts)
                    effettori.append(agent)

    return effettori


def read_nodi_essenziali(file_name):
    essenziali = []

    with open(file_name, "r", encoding="utf-8") as file:
        next_read = ""

        for line in file:
            if "ESSENZIALI" in line:
                next_read = "essenziali"

            if next_read == "essenziali":
                parts = line.split()
                if len(parts) == 2:
                    essenziali.append(int(parts[0]))

    return essenziali


def check_valori(agent_periodo, env_periodo, valori_ideali, nodi_effettori, nodi_essenziali, agent_n_genes):
    if agent_periodo == 0 or env_periodo == 0:
        raise ValueError("Errore espansione attrattori!")

    if not valori_ideali:
        raise ValueError("Errore calcolo valori ideali!")

    if not nodi_effettori:
        raise ValueError("Nessun nodo effettore!")

    for e in nodi_effettori:
        if e > agent_n_genes:
            raise ValueError("Numero nodo effettore non accettabile!")

    if not nodi_essenziali:
        raise ValueError("Nessun nodo essenziali!")

    for e in nodi_essenziali:
        if e > agent_n_genes:
            raise ValueError("Numero nodo essenziale non accettabile!")


def check_omega(omega):
    if omega <= 0 and omega != -1:
        raise ValueError("Valore omega non accettabile!")


def write_input_benessere_file(file_name, omega, nodi_essenziali, valori_ideali):
    with open(file_name, "w") as file:
        file.write(f"omega: {omega}\n")
        file.write("ELENCO NODI ESSENZIALI (ID NODO AGENTE - VALORE IDEALE)\n")

        for e in nodi_essenziali:
            file.write(f"{e}  {valori_ideali[e]}\n")


def read_benessere(file_name):
    with open(file_name, "r", encoding="utf-8") as file:
        benessere = file.readline().strip()
        return benessere


def write_output_benessere_file(file_name, benesseri):
    with open(file_name, "w") as file:
        for b in benesseri:
            file.write(f"{b["benessere"]}   ")
            for funzione in b["funzioni"]:
                for x in funzione:
                    file.write(f"{x}")
                file.write(f" ")
            file.write(f"\n")


def ricalcola_uscite_graph(n_uscite, bias_per_ogni_k, k_minimo):
    bias = bias_per_ogni_k[int(math.log2(n_uscite)) - k_minimo]
    new_uscite = generate_random_boolean_values(n_uscite, bias)
    return new_uscite


def genera_funzioni_booleane(rbn_agent, nodi_effettori, bias_per_ogni_k_agente, k_minimo):
    new_funzioni_nodi_effettori = []

    for e in nodi_effettori:
        new_uscite = ricalcola_uscite_graph(len(rbn_agent[e]["uscite"]), bias_per_ogni_k_agente, k_minimo)
        new_funzioni_nodi_effettori.append(new_uscite)

    return new_funzioni_nodi_effettori


def check_funzioni_booleane_uguali(benesseri, new_funzioni_nodi_effettori):
    for b in benesseri:
        if b["funzioni"] == new_funzioni_nodi_effettori:
            return True
    return False


def read_last_state(file_name):
    init_conditions = []

    last_state = None
    with open(file_name, "r") as f:
        for row in f:
            clean_row = row.strip()
            if clean_row:
                last_state = clean_row

    init_condition = [int(x) for x in last_state.strip().split()]
    init_conditions.append(init_condition)
    return init_conditions


def main():
    parser = argparse.ArgumentParser(description="Specifica se deve essere lanciato normalmente o se per l'evoluzione")
    parser.add_argument("-e", "--evolution", action="store_true", help="Eseguito per l'evoluzione (non modifica condizioni iniziali e profilo)")
    parser.add_argument( "-o", "--omega", type=int, default=-1, help="Valore omega (opzionale, default = periodo attrattore)")
    args = parser.parse_args()

    omega = args.omega
    check_omega(omega)

    parameters = read_file("benessere_interaction_simulator_input.txt")
    n_iterazioni = int(parameters["n_iterazioni"])
    mode = parameters["mode"].lower()

    check_parameters(n_iterazioni, mode)

    agent_n_genes, rbn_agent = read_graph(os.path.join("agent", "grafo_default.txt"))

    rbn_agent_iniziale = copy.deepcopy(rbn_agent)

    # Se viene lanciato dal file "evolution.py" non devo ricreare le condizioni iniziali e il profilo
    if not args.evolution:
        # Genero le condizioni iniziali
        subprocess.run(["python", "generator_initconditions.py", "-a", "-e"])

        # Simulo il comportamento dell'agente e dell'ambiente in mode 3
        subprocess.run(["python", "simulator.py", "-a", "-e"])

        # Trovo il rapporto degli attrattori
        subprocess.run(["python", "RBN_rapporto.py", "-a", "-e"])

        # Espando gli attrattori
        subprocess.run(["python", "espandi_attrattori.py", "-a", "-e"])

    # Leggo dati precedentemente calcolati
    agent_n_genes, agent_periodo, agent_init_condition = read_init_condition(os.path.join("agent", "attrattori_espansi.txt"))
    env_n_genes, env_periodo, env_init_condition = read_init_condition(os.path.join("environment", "attrattori_espansi.txt"))
    valori_ideali = read_valori_ideali(os.path.join("agent", "attrattori_espansi_media.txt"))
    nodi_essenziali = read_nodi_essenziali("input_benessere.txt")
    nodi_effettori = read_nodi_effettori("input_AG_AMB.txt")

    check_valori(agent_periodo, env_periodo, valori_ideali, nodi_effettori, nodi_essenziali, agent_n_genes)

    # Scrivo le nuove condizioni iniziali su file
    print_states(agent_n_genes, 1, agent_init_condition, os.path.join("agent", "cond_default.txt"))
    print_states(env_n_genes, 1, env_init_condition, os.path.join("environment", "cond_default.txt"))

    # Scrivo il omega = periodo e il valore ideale dei nodi essenziali solo se non è specificato come parametro
    if omega == -1:
        omega = agent_periodo
    write_input_benessere_file("input_benessere.txt", omega, nodi_essenziali, valori_ideali)

    # Lettura parametri necessari per riscrivere le funzioni booleane
    parameters_rbn_generator = read_file(os.path.join("agent", "input_generatore.txt"))
    bias_per_ogni_k_agente = list(map(float, parameters_rbn_generator["bias_per_ogni_k"].split()))
    k_minimo = int(parameters_rbn_generator["k_minimo"])

    benesseri = []

    for i in range(n_iterazioni):
        # Simulo interazione tra agente e ambiente -> calcola direttamente il benessere se in mode 2
        subprocess.run(["python", "agent_env_interaction.py", "-a", "-e"])

        funzioni_nodi_effettori = []
        benessere = read_benessere("benessere_agent.txt")

        # Memorizzo il valore delle ultime funzioni booleane
        for e in nodi_effettori:
            funzioni_nodi_effettori.append(rbn_agent[e]["uscite"])

        iterazione = {"benessere": benessere, "funzioni": funzioni_nodi_effettori}
        benesseri.append(iterazione)

        # Genero nuove funzioni booleane
        new_funzioni_nodi_effettori = genera_funzioni_booleane(rbn_agent, nodi_effettori, bias_per_ogni_k_agente, k_minimo)

        c = 0
        ciclo_infinito = False
        # Controllo che non sia già stata generata una funzione booleana uguale
        while check_funzioni_booleane_uguali(benesseri, new_funzioni_nodi_effettori):
            new_funzioni_nodi_effettori = genera_funzioni_booleane(rbn_agent, nodi_effettori, bias_per_ogni_k_agente, k_minimo)
            c += 1
            if c > 500:
                ciclo_infinito = True
                break

        if ciclo_infinito:
            break

        for j, e in enumerate(nodi_effettori):
            rbn_agent[e]["uscite"] = new_funzioni_nodi_effettori[j]

        print_grafo(agent_n_genes, rbn_agent, "agent")

        if mode == "b": # Condizione iniziale = ultimo stato raggiunto
            agent_last_state = (read_last_state(os.path.join("agent", "output_interaction_mode3.txt")))
            env_last_state = (read_last_state(os.path.join("environment", "output_interaction_mode3.txt")))

            # Scrivo le nuove condizioni iniziali su file
            print_states(agent_n_genes, 1, agent_last_state, os.path.join("agent", "cond_default.txt"))
            print_states(env_n_genes, 1, env_last_state, os.path.join("environment", "cond_default.txt"))

    write_output_benessere_file("benessere_interaction_simulator_output.txt", benesseri)

    # Ripristino la RBN iniziale
    print_grafo(agent_n_genes, rbn_agent_iniziale, "agent")


if __name__ == "__main__":
    main()