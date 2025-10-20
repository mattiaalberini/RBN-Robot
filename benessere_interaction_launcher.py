import os
import shutil
import subprocess
from decimal import Decimal
import pandas
import numpy

from utils import read_file


# Crea la cartella che conterrà gli N lanci
def crea_dir_lanci(nome_lanci):
    if not os.path.exists("risultati_lanci"):
        os.mkdir("risultati_lanci")

    dir = os.path.join("risultati_lanci", nome_lanci)
    counter = 1

    while os.path.exists(dir):
        dir = os.path.join("risultati_lanci", f"{nome_lanci}_{counter}")
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


# Conto il numero di attrattori: se uguale a 0 rigenero la RBN
def attrattore_trovato(file_name):
    # Leggo solo la prima riga del file
    with open(file_name, "r") as f:
        line = f.readline()

    # Divide la riga in parti
    parts = line.split()

    # Trova il valore dopo "Attrattori:"
    for i, p in enumerate(parts):
        if p == "Attrattori:":
            attrattori = int(parts[i + 1])

            if attrattori != 0:
                return True

    return False


def main():
    parameters = read_file("benessere_interaction_launcher_input.txt")
    nome_lanci = parameters["nome lanci"]
    n_lanci = int(parameters["n_lanci"])

    # Creo la cartella che conterrà gli N lanci
    dir_lanci = crea_dir_lanci(nome_lanci)

    # Per memorizzare i dati per il file excel
    dati = []

    for i in range(1, n_lanci+1):
        # Creo la cartella del lancio
        dir_lancio = os.path.join(os.getcwd(), dir_lanci, f"L{i}")
        os.mkdir(dir_lancio)

        # Creo nuove RBN e condizioni iniziali se specificato
        subprocess.run(["python", "agent_env_generator.py"])

        # Eseguo la simulazione
        subprocess.run(["python", "benessere_interaction_simulator.py", "-o", "4"])

        # Non ho trovato attrattori -> ripeto la simulazione
        while not attrattore_trovato(os.path.join("agent","output_motore_rapporto.txt")) or not attrattore_trovato(os.path.join("environment","output_motore_rapporto.txt")):
            print("Nessun attrattore trovato, rilancio!")
            subprocess.run(["python", "agent_env_generator.py"])
            subprocess.run(["python", "benessere_interaction_simulator.py", "-o", "4"])

        # Copio i file all'interno della cartella del relativo lancio
        shutil.copytree(os.path.join(os.getcwd(), "agent"), os.path.join(dir_lancio, "agent"), dirs_exist_ok=True)
        shutil.copytree(os.path.join(os.getcwd(), "environment"), os.path.join(dir_lancio, "environment"), dirs_exist_ok=True)

        for file in os.listdir(os.getcwd()):
            if file.endswith(".txt") and os.path.isfile(os.path.join(os.getcwd(), file)):
                shutil.copy2(os.path.join(os.getcwd(), file), dir_lancio)


        # Leggo il file senza specificare dtype per sapere quante colonne ci sono
        df_temp = pandas.read_csv(os.path.join(dir_lancio, "benessere_interaction_simulator_output.txt"), sep=r"\s+", header=None, nrows=1)
        n_colonne = df_temp.shape[1]
        # Costruisco il dict per dtype: prima colonna float, le altre stringhe
        dtype_dict = {0: float}
        for i in range(1, n_colonne):
            dtype_dict[i] = str

        # Memorizzo i dati necessari per il file excel
        df = pandas.read_csv(os.path.join(dir_lancio, "benessere_interaction_simulator_output.txt"), sep=r"\s+", header=None, dtype=dtype_dict)

        n_colonne = df.shape[1]
        nodi_essenziali = read_valore_ideale_nodi_essenziali("input_benessere.txt")
        profilo = [float(nodi_essenziali[x]) for x in nodi_essenziali]

        # Creo nuove colonne vuote
        for i in range(len(profilo)):
            df[n_colonne + i] = numpy.nan

        # Metto i valori solo nella prima riga
        df.loc[0, range(n_colonne, n_colonne + len(profilo))] = profilo

        # Tutte le nuove colonne devono essere float64
        mapping = {col: "float64" for col in range(n_colonne, df.shape[1])}
        df = df.astype(mapping)

        dati.append(df)
        dati.append(pandas.DataFrame([["", "", ""]]))  # Aggiungo una riga vuota

        print("")

    # Creo il file excel contenente la sintesi
    df_final = pandas.concat(dati, ignore_index=True)
    df_final.to_excel(os.path.join(dir_lanci, "sintesi.xlsx"), index=False, header=False)


if __name__ == "__main__":
    main()