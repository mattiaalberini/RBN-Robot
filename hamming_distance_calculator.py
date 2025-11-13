import os
import subprocess

import pandas as pd

from benessere_interaction_simulator import read_nodi_effettori
from evolution import find_best_benessere
from generator_RBN import print_grafo
from utils import read_graph


def find_benessere_zero(file_name):
    with open(file_name, "r") as f:
        for linea in f:
            colonne = linea.strip().split()
            if not colonne:
                continue
            benessere = float(colonne[0])  # Prima colonna (benessere)
            funzioni_booleane = colonne[1:]  # Altre colonne (funzioni booleane)

            if benessere == 0:
                return benessere, funzioni_booleane

    raise ValueError("Nessun benessere pari a 0 trovato!")


def crea_excel_file(file_name, output_file):
    with open(file_name, "r") as f:
        righe = f.readlines()

    righe = righe[2:] # Salta le prime due righe

    dati = []
    for riga in righe:
        if riga.strip():
            numeri = [int(x) for x in riga.strip().split()]
            dati.append(numeri)

    df = pd.DataFrame(dati)
    df.to_excel(output_file, index=False, header=False)


def main():
    nodi_effettori = read_nodi_effettori("input_AG_AMB.txt")
    benessere, funzioni_booleane = find_best_benessere("benessere_interaction_simulator_output.txt")

    agent_n_genes, rbn_agent = read_graph(os.path.join("agent", "grafo_default.txt"))

    for j, e in enumerate(nodi_effettori):
        rbn_agent[e]["uscite"] = funzioni_booleane[j]

    print_grafo(int(agent_n_genes), rbn_agent, "agent")

    subprocess.run(["python", "agent_env_interaction.py"])

    output_file = "variazione_nodi.xlsx"
    crea_excel_file(os.path.join("agent", "variazione_nodi.txt"), output_file)


if __name__ == "__main__":
    main()