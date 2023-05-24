import random


class Selection:
    def __init__(self, a, b, c):
        self.a = a
        self.b = b
        self.c = c
        self.fitness_population = []
        self.fitness_probabilities = []
        self.fitness_probability_intervals = []

    def generate_fitness(self, num):
        # the fitness function in this case will be the 2nd grade
        # equation with the corresponding parameters
        return self.a * num ** 2 + self.b * num + self.c

    def generate_fitness_for_population(self, population_values):
        self.fitness_population = []

        for chromosome_value in population_values:
            chromosome_fitness = self.generate_fitness(chromosome_value)
            self.fitness_population.append(chromosome_fitness)

    def generate_fitness_probabilities(self):
        # selection will be proportionate, each chromosome will have
        # the probability equal to fitness / overall_fitness_of_population
        self.fitness_probabilities = []
        total_fitness = sum(self.fitness_population)

        for fitness in self.fitness_population:
            self.fitness_probabilities.append(fitness / total_fitness)

    def generate_fitness_intervals(self):
        self.fitness_probability_intervals = []
        total_fitness = sum(self.fitness_population)

        for cnt in range(len(self.fitness_population) + 1):
            fitness_till__now = sum(self.fitness_population[:cnt])
            self.fitness_probability_intervals.append(fitness_till__now / total_fitness)

    def generate_chromosomes(self, printable=False, output_file=None):
        chromosome_indexes = []
        random_numbers = []
        population_size = len(self.fitness_population)
        output_format = "{}: u={}, corespunzator cromozomului {}\n"

        # taking into account the elitist selection, the chromosome with the
        # biggest value will be in the next generation as well
        chromosome_indexes.append(self.fitness_population.index(max(self.fitness_population)))
        if printable:
            output_file.write(output_format.format(1, "alegere elitista", chromosome_indexes[0] + 1))

        # generate population_size - 1 random numbers, find in which interval [i, i+1)
        # of fitness probability they fit in, choose the (i+1)th chromosome
        for cnt in range(population_size - 1):
            u = random.uniform(0, 1)
            random_numbers.append(u)
            desired_interval = 0

            # binary search to find the interval
            left, right = 0, len(self.fitness_probability_intervals) - 1
            while left <= right:
                mid = (left + right) // 2
                mid_left_closure = self.fitness_probability_intervals[mid]
                mid_right_closure = self.fitness_probability_intervals[mid + 1]

                if mid_left_closure <= u < mid_right_closure:
                    desired_interval = mid
                    break
                elif u >= mid_left_closure:
                    left = mid + 1
                else:
                    right = mid - 1

            chromosome_indexes.append(desired_interval)
            # +2 because the indexation starts from 0 and the first sport
            # is taken by the elitist choice
            if printable:
                output_file.write(output_format.format(cnt + 2, u, desired_interval + 1))

        if printable:
            output_file.write("\n")
        return chromosome_indexes

    def generate_fitness_statistics(self, output_file):
        max_fitness = max(self.fitness_population)
        mean_fitness = sum(self.fitness_population) / len(self.fitness_population)
        output_file.write(f"Max fitness: {'{:.20f}'.format(max_fitness)}, Mean fitness {'{:.20f}'.format(mean_fitness)}\n")
        return max_fitness, mean_fitness

    def generate_fitness_statistics_print(self):
        max_fitness = max(self.fitness_population)
        mean_fitness = sum(self.fitness_population) / len(self.fitness_population)
        print(f"Max fitness: {'{:.20f}'.format(max_fitness)}, Mean fitness {'{:.20f}'.format(mean_fitness)}\n")
        return max_fitness, mean_fitness