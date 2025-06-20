class RBN:
    def __init__(self, rbn_genes=None):
        self.genes = rbn_genes if rbn_genes is not None else []


    def add_gene(self,gene):
        self.genes.append(gene)


    def set_initconditions(self, initconditions):
        for i, stato in enumerate(initconditions):
            self.genes[i].set_stato(stato)


    def get_state(self):
        str_state = ""
        str_state += " ".join(str(gene.get_stato()) for gene in self.genes)

        return str_state


    def set_gene_stato(self, num_gene, stato):
        self.genes[num_gene].set_stato(stato)

    def get_gene_stato(self, num_gene):
        return self.genes[num_gene].get_stato()


    def __str__(self):
        str_genes = ""
        str_genes += "\n".join(str(gene) for gene in self.genes)
        return str_genes