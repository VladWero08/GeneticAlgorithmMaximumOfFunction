from codification import Codification
from population import Population, Display
from selection import Selection
from recombination import Recombination
from mutation import Mutation

input_file = open("io_files/input.in", "r")
output_file = open("io_files/output.out", "w")

population_size = int(input_file.readline()[:-1])
[left_closure, right_closure] = [int(num) for num in input_file.readline()[:-1].split()]
[a, b, c] = [int(num) for num in input_file.readline()[:-1].split()]
precision = int(input_file.readline()[:-1])
prob_recombination = int(input_file.readline()[:-1]) / 100
prob_mutation = int(input_file.readline()[:-1]) / 100
steps = int(input_file.readline())

# initiate the population & a codification, selection and display object
# with the current known values
population = Population(population_size, left_closure, right_closure, a, b, c, precision)
codif = Codification(left_closure, right_closure, precision)
select = Selection(a, b, c)
display = Display(population, select, output_file=output_file)

# Output the description of the algorithm at the begining
# of the output file
output_file.write("Algoritm genetic pentru determinarea maximului unei functii pozitive pe un domeniu dat.\n")
output_file.write(f"Functia pentru care va determina maximul este: {a} * x^2 + {b} * x + {c}, definita pe intervalul [{left_closure},{right_closure}].\n")
output_file.write(f"Dimensiunea populatiei = {population_size}. Precizia = {precision}. Probabilitatea de recombinare = {prob_recombination}. Probabilitatea de mutatie = {prob_mutation}. Numarul de etape = {steps}.\n\n")

##################################
########## First batch ###########
##################################

# generate the first population randomly
population.generate_all_chromosomes(codif)
# generate all the fitness measurement
select.generate_fitness_for_population(population.chromosomes_values)
output_file.write("Populatie initiala:\n")
output_file.write("-------------------\n")
display.display_population()

# generate probabilities
select.generate_fitness_probabilities()
output_file.write("Probabilitati de selectie:\n")
output_file.write("--------------------------\n")
display.display_probabilities()

# generate probability interval
select.generate_fitness_intervals()
output_file.write("Intevalele probabilitatilor de selectie:\n")
output_file.write("----------------------------------------\n")
display.display_probability_intervals()

# generate new chromosomes based on fitness value
output_file.write("Selectia de cromozomi:\n")
output_file.write("----------------------\n")
new_chromosomes_index = select.generate_chromosomes(printable=True, output_file=output_file)
population.transform_chromosomes(codif, new_chromosomes_index)
select.generate_fitness_for_population(population.chromosomes_values)

# display the new population
display = Display(population, select, output_file=output_file)
output_file.write("Dupa procesul de selectie:\n")
output_file.write("--------------------------\n")
display.display_population()

# define recombination and find which chromosomes to recombine
recombination = Recombination(population.chromosomes, population.chromosomes_values, prob_recombination,
                              codif.num_of_characteristics)
output_file.write("Cromozomii care vor fi recombinati:\n")
output_file.write("-----------------------------------\n")
chromosomes_to_recombine = recombination.generate_chromosomes_to_recombine(printable=True, output_file=output_file)
recombination.recombine_chromosomes(codif, chromosomes_to_recombine, printable=True, output_file=output_file)
population.chromosomes, population.chromosomes_values = recombination.chromosomes, recombination.chromosome_values
select.generate_fitness_for_population(population.chromosomes_values)

# display the new population
display = Display(population, select, output_file=output_file)
output_file.write("Dupa procesul de recombinare:\n")
output_file.write("--------------------------\n")
display.display_population()

# define mutation and find which chromosomes to mutate
mutation = Mutation(population.chromosomes, population.chromosomes_values, prob_mutation,
                    codif.num_of_characteristics)
chromosomes_to_mutate = mutation.generate_chromosomes_to_mutate(printable=True, output_file=output_file)
mutation.mutate_chromosomes(codif, chromosomes_to_mutate, printable=True, output_file=output_file)

population.chromosomes, population.chromosomes_values = mutation.chromosomes, mutation.chromosome_values
select.generate_fitness_for_population(population.chromosomes_values)

# display the new population
display = Display(population, select, output_file=output_file)
output_file.write("Dupa procesul de mutatie:\n")
output_file.write("--------------------------\n")
display.display_population()

max_evolution = []
mean_evolution = []
output_file.write("Etapa 1: ")
max_step_value, mean_step_value = select.generate_fitness_statistics(output_file)
max_evolution.append(max_step_value), mean_evolution.append(mean_step_value)

# for the rest of the steps, the only output will be the maximum
# value from a chromosome in the population and the mean value of the population
for step in range(steps - 1):
    output_file.write(f"Etapa {step + 2}: ")
    # recalculcate the metrics for fitness
    select.generate_fitness_probabilities()
    select.generate_fitness_intervals()

    # having that new metrics, randomly select another population
    # based on the current fitness levels
    new_chroms_based_on_fitness = select.generate_chromosomes()
    population.transform_chromosomes(codif, new_chroms_based_on_fitness)
    select.generate_fitness_for_population(population.chromosomes_values)

    # recombine the newly generated population,
    # afterwards mutate it
    # --------------------
    # recombination steps
    recombination = Recombination(population.chromosomes, population.chromosomes_values, prob_recombination,
                                  codif.num_of_characteristics)
    chromosomes_to_recombine = recombination.generate_chromosomes_to_recombine()
    recombination.recombine_chromosomes(codif, chromosomes_to_recombine)
    population.chromosomes, population.chromosomes_values = recombination.chromosomes, recombination.chromosome_values

    # mutation steps
    mutation = Mutation(population.chromosomes, population.chromosomes_values, prob_mutation,
                        codif.num_of_characteristics)
    chromosomes_to_mutate = mutation.generate_chromosomes_to_mutate()
    mutation.mutate_chromosomes(codif, chromosomes_to_mutate)
    population.chromosomes, population.chromosomes_values = mutation.chromosomes, mutation.chromosome_values

    select.generate_fitness_for_population(population.chromosomes_values)
    max_step_value, mean_step_value = select.generate_fitness_statistics(output_file)
    max_evolution.append(max_step_value), mean_evolution.append(mean_step_value)
