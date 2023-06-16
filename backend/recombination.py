import random

class Recombination:
    def __init__(self, chromosomes, chromosome_values, probability, num):
        self.chromosomes = chromosomes
        self.chromosome_values = chromosome_values
        self.probability = probability
        self.num_of_characteristics = num

    def list_to_string(self, list):
        return "".join(map(str, list))

    def generate_chromosomes_to_recombine(self, printable=False, output_file=None):
        chromosomes_to_recombine = []
        output_format = "{}: cromozom={}, probabilitate={}\n"
        output_format_valid = "{}: cromozom={}, probabilitate={} < {} deci va participa\n"

        for cnt, chrom in enumerate(self.chromosomes):
            prob = random.uniform(0, 1)
            if prob >= self.probability:
                if printable:
                    output_file.write(output_format.format(cnt+1, self.list_to_string(chrom), prob))
            else:
                chromosomes_to_recombine.append(cnt)
                if printable:
                    output_file.write(output_format_valid.format(cnt+1, self.list_to_string(chrom), prob, self.probability))

        if printable:
            output_file.write("\n")
        return chromosomes_to_recombine

    def recombine_chromosomes(self, codification, chrom_recombine, printable=False, output_file=None):
        # recombine the chromosome by applying crossover onto a pair of
        # two, until ther are not any left
        recombination_output = "Recombinare dintre cromozomii: \n   cromozomul {}: {}, cromozomul {}: {}, in punctul {}\n"
        result_output = "In urma recombinarii: \n   cromozomul {}: {}, cromozomul {}: {}\n"

        # if the number of chromosomes to recombine is odd, ignore the last one
        if len(chrom_recombine) % 2 != 0:
            # pop the last element from the list
            chrom_recombine.pop()

        # while there are chromosomes to recombine, the list has elements
        while len(chrom_recombine) != 0:
            # take two random indexes from the index list
            chrom_to_recomb_cnt_1 = random.randint(0, len(chrom_recombine) - 1)
            chrom_cnt_1 = chrom_recombine[chrom_to_recomb_cnt_1]
            chrom_recombine.pop(chrom_to_recomb_cnt_1)

            chrom_to_recomb_cnt_2 = random.randint(0, len(chrom_recombine) - 1)
            chrom_cnt_2 = chrom_recombine[chrom_to_recomb_cnt_2]
            chrom_recombine.pop(chrom_to_recomb_cnt_2)

            crossover_index = random.randint(0, self.num_of_characteristics)
            if printable:
                output_file.write(recombination_output.format(chrom_cnt_1 + 1, self.chromosomes[chrom_cnt_1], chrom_cnt_2 + 1, self.chromosomes[chrom_cnt_2], crossover_index))

            # crossover the randomly chosen chromosomes, also calculate
            # their new 'x' value
            new_chromosome_1 = self.chromosomes[chrom_cnt_1][:crossover_index] + self.chromosomes[chrom_cnt_2][crossover_index:]
            new_chromosome_2 = self.chromosomes[chrom_cnt_2][:crossover_index] + self.chromosomes[chrom_cnt_1][crossover_index:]
            # change the binary value
            self.chromosomes[chrom_cnt_1] = new_chromosome_1
            self.chromosomes[chrom_cnt_2] = new_chromosome_2
            # change the actual value, attribute the higher closure value
            self.chromosome_values[chrom_cnt_1] = codification.find_interval_for_bits_num(new_chromosome_1)[1]
            self.chromosome_values[chrom_cnt_2] = codification.find_interval_for_bits_num(new_chromosome_2)[1]

            if printable:
                output_file.write(result_output.format(chrom_cnt_1 + 1, new_chromosome_1, chrom_cnt_2 + 1, new_chromosome_2))

        if printable:
            output_file.write("\n")