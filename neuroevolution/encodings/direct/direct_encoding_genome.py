import tempfile
from graphviz import Digraph

from neuroevolution.encodings import BaseGenome
from neuroevolution.encodings.direct import DirectEncodingModel


class DirectEncodingGene:
    def __init__(self, gene_id, conn_in, conn_out):
        self.gene_id = gene_id
        self.conn_in = conn_in
        self.conn_out = conn_out


class DirectEncodingGenome(BaseGenome):
    def __init__(self, genome_id, genotype, activations, trainable):
        self.genome_id = genome_id
        self.genotype = genotype
        self.activations = activations
        self.trainable = trainable

        self.fitness = 0
        self.phenotype_model, self.topology_levels = self._create_phenotype_model()

    def __call__(self, *args, **kwargs):
        return self.phenotype_model(*args, **kwargs)

    def __str__(self):
        serialized_genotype, serialized_activations = self.serialize()
        string_repr = "Genome-ID: {} \t--- Fitness: {} \t--- Genotype: {} \t--- Activations: {}".format(
            self.genome_id, self.fitness, serialized_genotype, serialized_activations)
        return string_repr

    def serialize(self):
        # Convert genome into the explicit genotype and activation dicts that can also be supplied directly
        serialized_genotype = dict()
        for gene in self.genotype:
            serialized_genotype[gene.gene_id] = (gene.conn_in, gene.conn_out)

        return serialized_genotype, self.activations

    def summary(self):
        print(self)
        # Possibly print the phenotype.summary() in this function as well

    def visualize(self, filename=None, directory=None, view=True):
        filename = "graph_genome_{}".format(self.genome_id) if filename is None else filename
        directory = tempfile.mkdtemp() if directory is None else directory

        # Create Digraph and set graph orientaion
        dot = Digraph(name=filename)
        dot.attr(rankdir='BT')

        # Specify edges of Digraph
        edge_list = list()
        for gene in self.genotype:
            edge = ('{}'.format(gene.conn_in), '{}'.format(gene.conn_out))
            edge_list.append(edge)
        dot.edges(edge_list)

        # Highlight Input and Output Nodes
        with dot.subgraph(name='cluster_1') as dot_in:
            for node in self.topology_levels[0]:
                dot_in.node('{}'.format(node))
            dot_in.attr(label='inputs', color='blue')
        with dot.subgraph(name='cluster_2') as dot_out:
            for node in self.topology_levels[-1]:
                dot_out.node('{}'.format(node))
            dot_out.attr(label='outputs', color='grey')

        # Render graph and save it in the specified directory (or temporary dir) and view it if set
        dot.render(filename=filename, directory=directory, view=view, cleanup=True, format='png')

    def get_phenotype_model(self):
        return self.phenotype_model

    def get_genotype(self):
        return self.genotype

    def get_activations(self):
        return self.activations

    def get_topology_levels(self):
        return self.topology_levels

    def get_id(self):
        return self.genome_id

    def set_fitness(self, fitness):
        self.fitness = fitness

    def get_fitness(self):
        return self.fitness

    def _create_phenotype_model(self):
        phenotype_model = DirectEncodingModel(self.genotype, self.activations, self.trainable)
        topology_levels = phenotype_model.get_topology_dependency_levels()
        return phenotype_model, topology_levels
