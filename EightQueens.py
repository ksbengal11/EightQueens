import genetic, random

class EightQueens:
    def test(self, size = 8, mutation_prob = 0.001, population_size=10):
        geneSet = [i for i in range(size)]

        def fnGetFitness(genes):
            return get_fitness(genes, size)

        optimalFitness = 0
        genetic.get_best(fnGetFitness, geneSet, optimalFitness, 1000000, 0.001)

def get_fitness(genes, size):
    fitness = 0
    for i in range(len(genes)):
        fitness += genes.count(genes[i]) - 1
        for j in range(len(genes)):
            if (i != j):
                dx = abs(i -j)
                dy = abs(genes[i] - genes[j])
                if (dx == dy):
                    fitness += 1
    return fitness

if __name__ == '__main__':
    solver = EightQueens()
    
    print "Solution to the eight queens problem using genetic algorithms"
    print "Mutation proability = 0.1 %"
    print "Maximum iterations = 1000000"
    
    solver.test()