import os
import subprocess

from utils import print_states


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


def check_valori(agent_periodo, env_periodo, valori_ideali, nodi_essenziali, agent_n_genes):
    if agent_periodo == 0 or env_periodo == 0:
        raise ValueError("Errore espansione attrattori!")

    if not valori_ideali:
        raise ValueError("Errore calcolo valori ideali!")

    if not nodi_essenziali:
        raise ValueError("Nessun nodo essenziali!")

    for e in nodi_essenziali:
        if e > agent_n_genes:
            raise ValueError("Numero nodo essenziale non accettabile!")


def write_input_benessere_file(file_name, agent_periodo, nodi_essenziali, valori_ideali):
    with open(file_name, "w") as file:
        file.write(f"omega: {agent_periodo}\n")
        file.write("ELENCO NODI ESSENZIALI (ID NODO AGENTE - VALORE IDEALE)\n")
        print(valori_ideali)

        for e in nodi_essenziali:
            file.write(f"{e}  {valori_ideali[e]}\n")


def main():
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

    check_valori(agent_periodo, env_periodo, valori_ideali, nodi_essenziali, agent_n_genes)

    # Scrivo le nuove condizioni iniziali su file
    print_states(agent_n_genes, 1, agent_init_condition, os.path.join("agent", "cond_default.txt"))
    print_states(env_n_genes, 1, env_init_condition, os.path.join("environment", "cond_default.txt"))

    # Scrivo il omega = periodo e il valore ideale dei nodi essenziali
    write_input_benessere_file("input_benessere.txt", agent_periodo, nodi_essenziali, valori_ideali)

    # Simulo interazione tra agente e ambiente -> calcola direttamente il benessere se in mode 2
    subprocess.run(["python", "agent_env_interaction.py", "-a", "-e"])


if __name__ == "__main__":
    main()