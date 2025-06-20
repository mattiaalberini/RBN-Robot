class RBNGene:
    def __init__(self, gene_number, ingressi, uscite):
        self.gene = gene_number
        self.ingressi = ingressi
        self.uscite = uscite
        self.stato = None

    def set_stato(self, stato):
        self.stato = stato

    def get_stato(self):
        return self.stato

    def __str__(self):
        return (f"Nodo {self.gene}: ingressi={self.ingressi}, uscite={self.uscite}")