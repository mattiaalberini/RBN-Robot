import os
import random
import shutil
import subprocess
from decimal import Decimal

import pandas

from generator_RBN import print_grafo
from utils import read_file, read_graph


# Crea la cartella che conterrà le generazioni
def crea_dir_generazioni(nome_evoluzione):
    if not os.path.exists("risultati_evoluzione"):
        os.mkdir("risultati_evoluzione")

    dir = os.path.join("risultati_evoluzione", nome_evoluzione)
    counter = 1

    while os.path.exists(dir):
        dir = os.path.join("risultati_evoluzione", f"{nome_evoluzione}_{counter}")
        counter += 1

    os.mkdir(dir)

    return dir


def read_valore_ideale_nodi_essenziali(file_name):
    nodi_essenziali = {}

    with open(file_name, "r", encoding="utf-8") as file:
        next_read = ""

        for line in file:
            if ":" in line:
                next_read = ""
            elif "ESSENZIALI" in line:
                next_read = "essenziali"

            if next_read == "essenziali":
                parts = line.split()
                if len(parts) == 2:
                    nodo = int(parts[0])
                    val = Decimal(parts[1])
                    nodi_essenziali[nodo] = val

    return nodi_essenziali


def find_best_benessere(file):
    first_row = True

    with open(file, "r") as f:
        for linea in f:
            colonne = linea.strip().split()
            if not colonne:
                continue
            benessere = float(colonne[0])  # Prima colonna (benessere)
            funzioni_booleane = colonne[1:]  # Altre colonne (funzioni booleane)

            if first_row:
                best_benessere = benessere
                best_funzioni_booleane = funzioni_booleane
                first_row = False
            elif benessere < best_benessere:
                best_benessere = benessere
                best_funzioni_booleane = funzioni_booleane

    return best_benessere, best_funzioni_booleane


def read_nodi_effettori(file_name):
    effettori = []
    effettori_ambiente = []
    sensori_ambiente = [] # Nodi dell'ambiente su cui interagiscono i nodi sensori

    with open(file_name, "r", encoding="utf-8") as file:
        next_read = ""

        for line in file:
            if ":" in line:
                next_read = ""
            elif "EFFETTORI" in line:
                next_read = "effettori"
            elif "SENSORI" in line:
                next_read = "sensori"

            if next_read == "effettori":
                parts = line.split()
                if len(parts) == 2:
                    agent, env = map(int, parts)
                    effettori.append(agent)
                    effettori_ambiente.append(env)

            if next_read == "sensori":
                parts = line.split()
                if len(parts) == 2:
                    agent, env = map(int, parts)
                    sensori_ambiente.append(env)

    return effettori, effettori_ambiente, sensori_ambiente


def write_nodi_effettori(file_name, effettori_agente, effettori_ambiente):
    new_righe = []

    with open(file_name, "r") as file:
        in_effettori = False
        i = -1

        for line in file:
            if "EFFETTORI" in line:
                in_effettori = True
            elif "SENSORI" in line:
                in_effettori = False

            if in_effettori:
                if i >= 0:
                    coppia = str(effettori_agente[i]) + "\t" + str(effettori_ambiente[i]) + "\n"
                    new_righe.append(coppia)
                else:
                    new_righe.append(line)
                i += 1
            else:
                new_righe.append(line)

    with open(file_name, "w") as f:
        f.writelines(new_righe)


def generazione(dir_lanci, i, calcola_profilo, omega):
    # Creo la cartella della generazione
    dir_lancio = os.path.join(os.getcwd(), dir_lanci, f"G{i}")
    os.mkdir(dir_lancio)

    # Eseguo la simulazione
    if calcola_profilo:
        subprocess.run(["python", "benessere_interaction_simulator.py", "-o", str(omega)]) # Ricalcola il profilo e le condizioni iniziali
    else:
        subprocess.run(["python", "benessere_interaction_simulator.py", "-e", "-o", str(omega)]) # Non ricalcola il profilo e le condizioni iniziali
    best_benessere, best_funzioni_booleane = find_best_benessere("benessere_interaction_simulator_output.txt")

    # Copio i file all'interno della cartella del relativo lancio
    shutil.copytree(os.path.join(os.getcwd(), "agent"), os.path.join(dir_lancio, "agent"), dirs_exist_ok=True)
    shutil.copytree(os.path.join(os.getcwd(), "environment"), os.path.join(dir_lancio, "environment"),
                    dirs_exist_ok=True)

    for file in os.listdir(os.getcwd()):
        if file.endswith(".txt") and os.path.isfile(os.path.join(os.getcwd(), file)):
            shutil.copy2(os.path.join(os.getcwd(), file), dir_lancio)

    effettori_agente, effettori_ambiente, sensori_ambiente = read_nodi_effettori("input_AG_AMB.txt")

    return best_benessere, best_funzioni_booleane, effettori_ambiente


# Modifica le funzioni booleane dei nodi effettori dell'agente e il nodo dell'ambiente su cui agisce
def modifica_agente(best_funzioni_booleane, effettori_agente, effettori_ambiente, new, sensori_ambiente):
    agent_n_genes, rbn_agent = read_graph(os.path.join("agent", "grafo_default.txt"))
    env_n_genes, rbn_env = read_graph(os.path.join("environment", "grafo_default.txt"))

    if new:
        pos_nodo_effettore = random.randint(0, len(effettori_ambiente) - 1)  # Quale nodo effettore modificare
        new_nodo_ambiente = random.randint(0, int(env_n_genes) - 1)  # Quale nodo dell'ambiente deve toccare
        while new_nodo_ambiente in effettori_ambiente or new_nodo_ambiente in sensori_ambiente:
            new_nodo_ambiente = random.randint(0, int(env_n_genes) - 1)

        effettori_ambiente[pos_nodo_effettore] = new_nodo_ambiente

    write_nodi_effettori("input_AG_AMB.txt", effettori_agente, effettori_ambiente)

    for j, e in enumerate(effettori_agente):
        rbn_agent[e]["uscite"] = best_funzioni_booleane[j]

    print_grafo(int(agent_n_genes), rbn_agent, "agent")


def main():
    parameters = read_file("evolution_input.txt")
    nome_evoluzione = parameters["nome evoluzione"]
    n_generazioni = int(parameters["n massimo generazioni"])
    omega = int(parameters.get("omega", -1))

    # Creo la cartella che conterrà gli N lanci
    dir_lanci = crea_dir_generazioni(nome_evoluzione)

    # Per memorizzare i dati per il file excel
    dati = []

    # Genero il padre (G0)
    best_benessere, best_funzioni_booleane, best_effettori_ambiente = generazione(dir_lanci, 0, True, omega)

    if best_benessere == 0:
        benessere_zero = True
    else:
        benessere_zero = False

    benessere_padre = best_benessere
    funzioni_booleane_padre = best_funzioni_booleane
    effettori_ambiente_padre = best_effettori_ambiente

    nodi_essenziali = read_valore_ideale_nodi_essenziali("input_benessere.txt")

    colonne = (
        ["Benessere"]
        + [""]
        + ["Nodo ambiente"] * len(best_effettori_ambiente)
        + [""]
        + ["Funzione booleane"] * len(best_funzioni_booleane)
        + [""]
        + ["Profilo"] * len(nodi_essenziali)
        + [""]
        + ["Migliore"]
    )

    riga = [best_benessere, ""]
    for e in best_effettori_ambiente:
        riga.append(e)
    riga.append("")
    for f in best_funzioni_booleane:
        riga.append(f)
    riga.append("")
    for n in nodi_essenziali:
        riga.append(nodi_essenziali[n])
    riga.append("")
    riga.append("S")

    dati.append(riga)

    i = 1
    while i < n_generazioni and not benessere_zero:
        print("")

        effettori_agente, effettori_ambiente, sensori_ambiente = read_nodi_effettori("input_AG_AMB.txt")

        modifica_agente(funzioni_booleane_padre, effettori_agente, effettori_ambiente, True, sensori_ambiente)
        best_benessere, best_funzioni_booleane, best_effettori_ambiente = generazione(dir_lanci, i, False, omega)

        nodi_essenziali = read_valore_ideale_nodi_essenziali("input_benessere.txt")

        riga = [best_benessere, ""]
        for e in effettori_ambiente:
            riga.append(e)
        riga.append("")
        for f in best_funzioni_booleane:
            riga.append(f)
        riga.append("")
        for n in nodi_essenziali:
            riga.append(nodi_essenziali[n])
        riga.append("")

        if best_benessere <= benessere_padre:
            if best_benessere == benessere_padre:
                migliore = "N"
            else:
                migliore = "S"

            benessere_padre = best_benessere
            funzioni_booleane_padre = best_funzioni_booleane
            effettori_ambiente_padre = effettori_ambiente

            print("Tengo il figlio")
        else:
            modifica_agente(funzioni_booleane_padre, effettori_agente, effettori_ambiente_padre, False, sensori_ambiente)
            migliore = "N"
            print("Torno al padre")

        riga.append(migliore)
        dati.append(riga)

        if best_benessere == 0:
            benessere_zero = True

        i += 1

    df = pandas.DataFrame(dati, columns=colonne)
    df.to_excel(os.path.join(dir_lanci, "sintesi.xlsx"), index=False)


if __name__ == "__main__":
    main()