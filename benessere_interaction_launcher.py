import os
import shutil
import subprocess
import pandas

from utils import read_file


# Crea la cartella che conterrà gli N lanci
def crea_dir_lanci(nome_lanci):
    dir = os.path.join(os.getcwd(), "risultati_lanci", nome_lanci)
    counter = 1

    while os.path.exists(dir):
        dir = os.path.join(os.getcwd(), "risultati_lanci", f"{nome_lanci}_{counter}")
        counter += 1

    os.mkdir(dir)

    return dir


def main():
    parameters = read_file("benessere_interaction_launcher_input.txt")
    nome_lanci = parameters["nome lanci"]
    n_lanci = int(parameters["n_lanci"])

    # Creo la cartella che conterrà gli N lanci
    dir_lanci = crea_dir_lanci(nome_lanci)

    for i in range(1, n_lanci+1):
        # Creo la cartella del lancio
        dir_lancio = os.path.join(os.getcwd(), dir_lanci, f"L{i}")
        os.mkdir(dir_lancio)

        # Eseguo la simulazione
        subprocess.run(["python", "benessere_interaction_simulator.py"])

        # Copio i file all'interno della cartella del relativo lancio
        shutil.copytree(os.path.join(os.getcwd(), "agent"), os.path.join(dir_lancio, "agent"), dirs_exist_ok=True)
        shutil.copytree(os.path.join(os.getcwd(), "environment"), os.path.join(dir_lancio, "environment"), dirs_exist_ok=True)

        for file in os.listdir(os.getcwd()):
            if file.endswith(".txt") and os.path.isfile(os.path.join(os.getcwd(), file)):
                shutil.copy2(os.path.join(os.getcwd(), file), dir_lancio)

        # Creo il file excel contenente la sintesi
        dati = []
        df = pandas.read_csv(os.path.join(dir_lancio, "benessere_interaction_simulator_output.txt"), sep=r"\s+", header=None)

        print(df)

        print("")


if __name__ == "__main__":
    main()