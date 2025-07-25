import os
from decimal import Decimal, getcontext

from utils import get_args, read_graph, simulate_step


def read_params(directory):
    file_name = os.path.join(directory, "output_motore_rapporto.txt")
    with open(file_name, 'r') as file:
        first_line = file.readline()
        parts = first_line.strip().split()
        attrattori = int(parts[1])
        geni = int(parts[3])

        data = []

        for line in file:
            pair = {}
            parts = line.strip().split()
            attrattore = list(map(int, parts[:geni]))
            periodo = int(parts[geni])
            #steps = float(parts[geni + 1])

            pair["attrattore"] = attrattore
            pair["periodo"] = periodo

            data.append(pair)

    return data


def espandi_attrattori(data, directory):
    file_name = os.path.join(directory, "grafo_default.txt")
    n_genes, graph = read_graph(file_name)

    attrattori_espansi = []
    attrattori_espansi_media = []

    for d in data:
        state = d["attrattore"]
        periodo = d["periodo"]

        states = [state]
        somma = state

        for i in range(periodo - 1):
            new_state = simulate_step(state, graph)
            state = new_state
            states.append(state)

            somma = [Decimal(str(a)) + Decimal(str(b)) for a, b in zip(somma, state)]

        attrattori_espansi.append(states)
        media = [Decimal(str(x)) / Decimal(str(periodo)) for x in somma]
        attrattori_espansi_media.append(media)

    return n_genes, attrattori_espansi, attrattori_espansi_media


def print_attrattori_espansi(n_genes, attrattori_espansi, n_cond, directory):
    file_name = os.path.join(directory, "attrattori_espansi.txt")
    with open(file_name, "w") as file:
        file.write(f"n_genes: {n_genes} n_cond: {n_cond}\n")

        for attrattore in attrattori_espansi:
            for stato in attrattore:
                file.write(f"{' '.join(str(x) for x in stato)}\n")
            file.write("\n")


def print_attrattori_espansi_media(n_genes, attrattori_espansi_media, n_cond, directory):
    file_name = os.path.join(directory, "attrattori_espansi_media.txt")
    with open(file_name, "w") as file:
        file.write(f"n_genes: {n_genes} n_cond: {n_cond}\n")

        for attrattore in attrattori_espansi_media:
            file.write(f"{'\t'.join(f'{x:.6f}' for x in attrattore)}\n")


def espandi_entity(directory):
    data = read_params(directory)
    n_genes, attrattori_espansi, media = espandi_attrattori(data, directory)

    print_attrattori_espansi(n_genes, attrattori_espansi, len(data), directory)
    print_attrattori_espansi_media(n_genes, media, len(data), directory)


def main():
    getcontext().prec = 6
    args = get_args()

    if args.agent:
        espandi_entity("agent")
        print("Attrattori agente espansi")
    if args.env:
        espandi_entity("environment")
        print("Attrattori ambiente espansi")
    if not args.agent and not args.env:
        print("Nessun parametro fornito. Usa -a e/o -e per espandere gli attrattori.")


if __name__ == "__main__":
    main()