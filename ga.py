#!/usr/bin/env python3
#
# How to run: python3 bonus1.py <population_size> <number_of_generations> <crossover_rate> <mutation_rate>
# e.g.: python3 bonus1.py 300 20 0.5 0.01

import sys
import math
import random

# Parameters
size = int(sys.argv[1])
generations = int(sys.argv[2])
p_crossover = float(sys.argv[3])
p_mutation = float(sys.argv[4])


class Member:
    def encoding(self, x): # Base10 to Base2
        return ('{0:b}'.format(int(x)))

    def decoding(self, x):
        base10 = int(x, 2) # Convert binary to decimal
        xi = -1.0 + (base10 * (3/(math.pow(2,22)-1)))
        return (format(xi, '1.6f'))

    def generate_chromosome(self):
        max = math.pow(2,22)
        self.chromosome = self.encoding(random.randrange(max))
        while len(self.chromosome) < 22:
            self.chromosome = '0' + self.chromosome
        return (self.chromosome)

    def get_fitness(self, x):
        return(float(self.decoding(str(x))))

    def __init__(self, chromosome=None):
        if chromosome is None:
            self.chromosome = self.generate_chromosome()
        else:
            self.chromosome = chromosome
        self.fitness = self.get_fitness(self.chromosome)



class Population:
    def generate_population(self):
        for i in range(0, self.population_size):
            # Generate new Member and append to population
            self.population.append(Member())

    def get_average_fitness(self):
        avg = 0
        for p in self.population:
            avg = avg + p.fitness
        return(avg/len(self.population))

    def get_fittest_member(self):
        fittest = 0
        member = ''
        for p in self.population:
            if p.fitness > fittest:
                fittest = p.fitness
                member = int(p.chromosome,2)
        return([fittest, member])

    def selection(self, average):
        for i, p in enumerate(self.population):
            if p.fitness < average:
                # print("Removing", p.chromosome, "with fitness", p.fitness)
                del self.population[i]

    def apply_operators(self, average_fitness):
        # selection
        # print("- Performing eugenics...")
        self.selection(average_fitness)

        # crossover and mutation

        # - split population
        halfpoint = int(len(self.population)/2)
        p1 = self.population[0:halfpoint]
        p2 = self.population[halfpoint:]

        # - iterate through parents to mate
        end = 999
        if len(p1) < len(p2):
            end = len(p1)
        else:
            end = len(p2)

        child = None
        for i in range(end):
            P = random.uniform(0,1)
            # Get crossover index
            crossover_index = random.randrange(22)

            if P <= p_crossover:
                # print("- Crossing over...")
                parent_1 = p1[i].chromosome
                parent_2 = p2[i].chromosome
                if P <= p_crossover: # Not really necessary, but it'll help with diversity
                    child = parent_1[0:crossover_index] + parent_2[crossover_index:22]
                else:
                    child = parent_2[0:crossover_index] + parent_1[crossover_index:22]

            # mutation
            P = random.uniform(0,1)
            if child is not None: # if a child was made
                if P <= p_mutation:
                    # print("- Mutating at P =", P)
                    random_index = random.randrange(22)
                    child = list(child)
                    if child[random_index] == '1':
                        child[random_index] = '0'
                    else:
                        child[random_index] = '1'
                    child = ''.join(child)
                    # print("-- After mutation:", child)

                # Add child to population
                self.population.append(Member(child))


    def __init__(self, size):
        self.population_size = size
        self.population = list()
        self.generate_population()


if __name__ == "__main__":
    print("Generating population...", end=' ')
    population = Population(size)
    print('\033[32m' + "Done!" + '\033[0m')

    number_of_generations = 0
    for i in range(generations):
        print("\n=======================\nGeneration", i+1)
        print("Average fitness:", end=' ')
        average_fitness = population.get_average_fitness()
        print(average_fitness)

        print("\nApplying operators...", end=' ')
        population.apply_operators(average_fitness)
        print('\033[32m' + "Done!" + '\033[0m')

        print("\nBest Candidate: ")
        fittest = population.get_fittest_member()
        print("Fitness:", fittest[0], "Value:", fittest[1])

        # termination condition: if average fitness is the same as best fitness or fitness is 2
        if average_fitness == fittest[0]:
            print("\nActivated termination condition:", average_fitness, "==", fittest[0])
            break
        if fittest[0] == 2:
            print("\nActivated termination condition: fittest == 2")
            break
        number_of_generations = i+1

    print("=======================\n")
    print("It took", number_of_generations, "generations to reach", fittest[0], "fitness with chromosome", '{0:b}'.format(int(fittest[1])))
