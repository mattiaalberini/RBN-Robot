# Crea la cartella che conterrà gli N lanci
import os
import shutil
import subprocess
from pathlib import Path

import pandas as pd

from utils import read_file


def crea_dir_lanci(nome_lanci):
    dir_name = "risultati_lanci_evoluzione"

    if not os.path.exists(dir_name):
        os.mkdir(dir_name)

    dir = os.path.join(dir_name, nome_lanci)
    counter = 1

    while os.path.exists(dir):
        dir = os.path.join(dir_name, f"{nome_lanci}_{counter}")
        counter += 1

    os.mkdir(dir)

    return dir


def check_evolution_dir_names(evolution, evolution_launcher):
    if evolution != evolution_launcher:
        raise ValueError("Nome cartella 'evoluzione' e 'evoluzione_launcher' diverse!")

    if os.path.exists("risultati_evoluzione"):
        raise ValueError("Eliminare cartella 'risultati_evoluzione'!")


def is_evolution_first_benessere_zero(dir_name):
    cartella = Path("risultati_evoluzione", dir_name)

    contenuti = list(cartella.iterdir())

    # Controllo preciso
    condizione = (
            len(contenuti) == 2 and
            any(p.is_dir() and p.name == "G0" for p in contenuti) and
            any(p.is_file() and p.name == "sintesi.xlsx" for p in contenuti)
    )

    if condizione:
        # La cartella contiene solo G0 e sintesi.xlsx"
        return True

    return False


def delete_dir(path):
    cartella = Path(path)
    shutil.rmtree(cartella)


def create_excel(path):
    cartella = Path(path)

    file_excel = sorted(cartella.rglob("*.xlsx"))

    dati_uniti = []

    for f in file_excel:
        # Legge il file Excel
        df = pd.read_excel(f, dtype=object, engine="openpyxl")

        # Aggiunge i dati del file
        dati_uniti.append(df)

        # Aggiunge una riga vuota
        dati_uniti.append(pd.DataFrame([[""] * len(df.columns)], columns=df.columns))

    # Unisce tutto in un unico DataFrame
    df_finale = pd.concat(dati_uniti, ignore_index=True, sort=False)

    # Salva nel file Excel finale
    output = cartella / "sintesi.xlsx"
    df_finale.to_excel(output, index=False)


def main():
    parameters_evoluzione = read_file("evolution_input.txt")
    nome_evoluzione = parameters_evoluzione["nome evoluzione"]

    parameters = read_file("evolution_launcher_input.txt")
    nome_lanci_evoluzione = parameters["nome lanci evoluzione"]
    n_lanci = int(parameters["n_lanci"])

    check_evolution_dir_names(nome_evoluzione, nome_lanci_evoluzione)

    # Creo la cartella che conterrà gli N lanci
    dir_lanci = crea_dir_lanci(nome_lanci_evoluzione)

    # Per memorizzare i dati per il file excel
    dati = []

    c_benessere_zero = 0    # Conta il numero di evoluzioni partite con benessere = 0
    i = 1
    while i < (n_lanci + 1):
        # Creo la cartella del lancio

        print(f"Lancio: {i}")

        # Creo nuove RBN e condizioni iniziali se specificato
        subprocess.run(["python", "agent_env_generator.py"])

        # Eseguo la simulazione
        subprocess.run(["python", "evolution.py"])

        if i == 1:
            app_nome_dir_evoluzione = nome_evoluzione
        else:
            app_nome_dir_evoluzione = nome_evoluzione + "_" + str(i - 1)

        # Controllo se in "risultati_evoluzione\nome_evoluzione" sono presenti solamente la cartella G0 e sintesi.xlsx
        # Se ci sono solamente questi due file vuol dire che il primo agente che ho generato ha dato subito benessere = 0
        first_benessere_is_zero = is_evolution_first_benessere_zero(app_nome_dir_evoluzione)

        if first_benessere_is_zero:
            # Rimuovo la carta dell'evoluzione che ha prodotto subito un benessere = 0
            del_dir_path = os.path.join("risultati_evoluzione", app_nome_dir_evoluzione, "G0")
            delete_dir(del_dir_path)
            os.remove(os.path.join("risultati_evoluzione", app_nome_dir_evoluzione, "sintesi.xlsx"))
            os.rmdir(os.path.join("risultati_evoluzione", app_nome_dir_evoluzione))

            c_benessere_zero += 1

            i -= 1

        i += 1
        print("")

    print(c_benessere_zero)

    # Copio i risultati delle evoluzioni nella cartella del lancio
    origine = "risultati_evoluzione"
    destinazione = dir_lanci
    shutil.copytree(origine, destinazione, dirs_exist_ok=True)

    # Creo il file excel
    create_excel(dir_lanci)


if __name__ == "__main__":
    main()