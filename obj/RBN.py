class RBN:
    def __init__(self, rbn_genes=None):
        self.genes = rbn_genes if rbn_genes is not None else []

    def add_gene(self,gene):
        self.genes.append(gene)

    def __str__(self):
        str_genes = ""
        str_genes += "\n".join(str(gene) for gene in self.genes)
        return str_genes