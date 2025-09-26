import os
import shutil
import subprocess
from decimal import Decimal
import pandas
import numpy

from utils import read_file


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


# Lettore parametri da file
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


def find_best_benessere():
    return -1


def main():
    parameters = read_file("evolution_input.txt")
    nome_evoluzione = parameters["nome evoluzione"]
    n_generazioni = int(parameters["n massimo generazioni"])

    # Creo la cartella che conterrà gli N lanci
    dir_lanci = crea_dir_generazioni(nome_evoluzione)

    # Per memorizzare i dati per il file excel
    dati = []

    i = 0
    benessere_zero = False
    while i < n_generazioni and not benessere_zero:
        # Creo la cartella della generazione
        dir_lancio = os.path.join(os.getcwd(), dir_lanci, f"G{i}")
        os.mkdir(dir_lancio)

        # Eseguo la simulazione
        subprocess.run(["python", "benessere_interaction_simulator.py"])

        # Copio i file all'interno della cartella del relativo lancio
        shutil.copytree(os.path.join(os.getcwd(), "agent"), os.path.join(dir_lancio, "agent"), dirs_exist_ok=True)
        shutil.copytree(os.path.join(os.getcwd(), "environment"), os.path.join(dir_lancio, "environment"), dirs_exist_ok=True)

        for file in os.listdir(os.getcwd()):
            if file.endswith(".txt") and os.path.isfile(os.path.join(os.getcwd(), file)):
                shutil.copy2(os.path.join(os.getcwd(), file), dir_lancio)


        i += 1


if __name__ == "__main__":
    main()