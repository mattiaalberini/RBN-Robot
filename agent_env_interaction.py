import os

from obj.RBN import RBN
from obj.RBNGene import RBNGene


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


def main():
    rbn_agent = load_graph(os.path.join("agent", "grafo_default.txt"))
    rbn_env = load_graph(os.path.join("environment", "grafo_default.txt"))

    print(rbn_agent)
    print(rbn_env)


if __name__ == "__main__":
    main()