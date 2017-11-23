import random

class Chromosome:
    Genes = None
    Fitness = None

    def __init__(self, genes, fitness):
        self.Genes = genes
        self.Fitness = fitness

class Population:
    Queens = None
    PopulationSize = None
    population = []
    weights = []

    def __init__(self, Queens = 8, Size = 10):
        self.Queens = Queens
        self.PopulationSize = Size

    def __getitem__(self, index):
        return self.population[index]

    def __len__(self):
        return len(self.population)

    def generatePopulation(self, geneSet, get_fitness):
        """
        Append chromosomes to the population list and sort by chromosomes with the highest fitness
            
        @arg geneSet Pool of genes
        @arg get_fitness Function for calculating the gene fitness
        @return population Population of chromosomes
        """
        for index in range(self.PopulationSize):
            newChromosome = _generate_parent(self.Queens, geneSet, get_fitness)
            self.population.append(newChromosome)
            self.weights.append((100 - newChromosome.Fitness)/100)

        return sorted(self.population,  key=lambda Chromosome:Chromosome.Fitness)

    def replaceChromosome(self, old, new):
        """
        Replace a chromosome in the population
        @arg old Chromosome to be replaced
        @arg new New chromosome
        """
        self.population.remove(old)
        self.population.append(new)

def _generate_parent(length, geneSet, get_fitness):
    """
    Function for generating a random chromosome

    @arg length Length of the gene (8 or n queens)
    @arg geneSet Combinations available for genes
    @arg getfitness Function for calcuating gene fitness
    @return New chromosome with random genes
    """
    genes = []
    while len(genes) < length:
        sampleSize = min(length - len(genes), len(geneSet))
        genes.extend(random.sample(geneSet, sampleSize))
    fitness = get_fitness(genes)
    return Chromosome(genes, fitness)

def _mutate(parent, geneSet, get_fitness):
    """
    Modify one index in the parent genes

    @arg parent Parent genes that will undergo mutation
    @arg geneSet One parent gene will be swapped with a gene from this set
    @arg get_fitness Function for calculating the fitness of the mutated gene
    @return Mutated chromosome
    """
    index = random.randrange(0, len(parent.Genes))
    childGenes = parent.Genes[:]
    newGene, alternateGene = random.sample(geneSet, 2)
    if childGenes[index] == newGene:
        childGenes[index] = alternateGene
    else:
        childGenes[index] = newGene
    
    fitness = get_fitness(childGenes)
    return Chromosome(childGenes, fitness)
    
def _crossover(geneSet_1, geneSet_2, genePool, get_fitness):
    """
    Crossing over two chromosomes to form a new one. If both gene sets share a gene at 
    a particular index the child will inherit that gene, otherwise the child will be 
    randomly assigned a gene from the genePool

    @arg geneSet_1 Set of genes that will be crossed over with geneSet_2
    @arg geneSet_2 Set of genes that will be crossed over with geneSet_1
    @arg geenPool Pool of possible genes to choose from for the new child
    @arg get_fitness Function for calculating the fitness of the new gene
    @returns Chromosome of the child after cross over
    """
    genePool = [i for i in range(len(geneSet_1))]
    newGene = [-1 for i in range(len(geneSet_1))]

    #FUTURE: Concatenate elements of parents together based on fitness
    for i in range(len(geneSet_1)):
        if (geneSet_1[i] == geneSet_2[i]):
            newGene[i] = geneSet_1[i]
            genePool.remove(newGene[i])

    for i in range(len(geneSet_2)):
        if (newGene[i] == -1):
            newGene[i] = random.choice(genePool)
            genePool.remove(newGene[i])

    fitness = get_fitness(newGene)
    return Chromosome(newGene, fitness)

def get_best(get_fitness, geneSet, optimalFitness, max_iterations, mutation_probability):
    """
    Function for finding the gene combination with the optimal fitness

    @arg get_fitness Function for calcuating the fitness of the solution gene
    @arg geneSet Available pool of genes to choose from
    @arg optimalFitness Desired fitness of the solution
    @arg maximum_iterations Maximum iterations allowed for finding the solution
    @arg mutation_probability Probability that a mutation will occur
    """
    population = Population()
    population.generatePopulation(geneSet, get_fitness)
    solution_found = False

    for i in range(max_iterations):

        #FUTURE: Select parents based on their weighted probability
        parent_1 = population[0] 
        parent_2 = population[1]
        parent_3 = population[len(population) - 1] #Chromosome with the lowest fitness is selected for replacement

        newChromosome = _crossover(parent_1.Genes, parent_2.Genes, geneSet, get_fitness)
        population.replaceChromosome(parent_3, newChromosome)

        if (random.random() < mutation_probability):
            newChromosome = _mutate(newChromosome, geneSet, get_fitness)

        if newChromosome.Fitness == optimalFitness:
            print "Solution found in {0} iterations".format(i)
            solution_found = True
            break

    if not solution_found: 
        print "Solution not found"