import random

class Mutation:
    def __init__(self, chromosomes, chromosome_values, probability, num):
        self.chromosomes = chromosomes
        self.chromosome_values = chromosome_values
        self.probability = probability
        self.num_of_characteristics = num

    def generate_chromosomes_to_mutate(self, printable=False, output_file=None):
        chromosomes_to_mutate = []

        for cnt, chrom in enumerate(self.chromosomes):
            prob = random.uniform(0, 1)
            if prob < self.probability:
                chromosomes_to_mutate.append(cnt)

        if printable:
            output_file.write("\n")
        return chromosomes_to_mutate

    def mutate_chromosomes(self, codification, chrom_mutate, printable=False, output_file=None):
        if printable:
            output_file.write(f"Probabilitate de mutatie este de: {self.probability}\n")

        if len(chrom_mutate) > 0:
            # generate an index for a characterstic of a chromosome
            gene = random.randint(0, self.num_of_characteristics)
            if printable:
                output_file.write("Cromozomii care vor fi modificati sunt: ")
            for chromosome in chrom_mutate:
                if printable:
                    output_file.write(f"{chromosome+1} ")
                # modify the characterstic and recalculate the value
                self.chromosomes[chromosome][gene-1] = 1 if self.chromosomes[chromosome] == 0 else 0
                self.chromosome_values[chromosome] = codification.find_interval_for_bits_num(self.chromosomes[chromosome])[1]

            if printable:
                output_file.write(f"\nGena care va fi mutata este: {gene}\n\n")
        else:
            if printable:
                output_file.write("Niciun cromozom nu va fi mutat.\n\n")