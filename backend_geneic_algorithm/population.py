import random
from selection import Selection

class Population:
    def __init__(self, population_size, left_closure, right_closure, a, b, c, precision):
        self.population_size = population_size
        self.left_closure = left_closure
        self.right_closure = right_closure
        self.a = a
        self.b = b
        self.c = c
        self.precision = precision

        self.chromosomes = []
        self.chromosomes_values = []

    def generate_chromosome(self, codification, num = None):
        # for a newly generated number, find the discretization interval which
        # it belongs to, than append those 2 values to the corresponding vectors
        if num is None:
            new_number = random.uniform(self.left_closure, self.right_closure)
        else:
            new_number = num
        new_number_bits = codification.find_interval_for_decimal_num(new_number)

        self.chromosomes.append(new_number_bits)
        self.chromosomes_values.append(new_number)

    def generate_all_chromosomes(self, codification):
        for cnt in range(self.population_size):
            self.generate_chromosome(codification)

    def transform_chromosomes(self, codification, chromosomes_indexes):
        # after new random set of chromosomes were generated, based on the
        # current chromosomes and their fitness level, modify the current chromosomes
        chromosomes_copy = [x for x in self.chromosomes_values]
        self.chromosomes = []
        self.chromosomes_values = []

        for chrom_cnt in chromosomes_indexes:
            self.generate_chromosome(codification, chromosomes_copy[chrom_cnt])

class Display:
    def __init__(self, population, select, output_file):
        # population --> Population() object
        # select --> Select() object
        self.population = population
        self.select = select
        self.output_file = output_file

    def list_to_string(self, list):
        return "".join(map(str, list))

    def display_population(self):
        output_format = "{}: {}, x={}, f(x)={}\n"

        for cnt in range(self.population.population_size):
            self.output_file.write(output_format.format(cnt + 1, self.list_to_string(self.population.chromosomes[cnt]), self.population.chromosomes_values[cnt],
                                       self.select.fitness_population[cnt]))
        self.output_file.write("\n")

    def display_probabilities(self):
        output_format = "cromozom {}, probabilitate={}\n"

        for cnt, probability in enumerate(self.select.fitness_probabilities):
            self.output_file.write(output_format.format(cnt + 1, probability))
        self.output_file.write("\n")

    def display_probability_intervals(self):
        output_format = "Intervalul {}: [{}, {})\n"

        for cnt in range(len(self.select.fitness_probability_intervals) - 1):
            self.output_file.write(output_format.format(cnt+1, self.select.fitness_probability_intervals[cnt], self.select.fitness_probability_intervals[cnt+1]))
        self.output_file.write("\n")