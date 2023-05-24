import json
from flask import Flask, after_this_request, request
from codification import Codification
from population import Population, Display
from selection import Selection
from recombination import Recombination
from mutation import Mutation

app = Flask(__name__)

@app.route("/")
def server_started():
    return "</p>Server is working!</p>"

@app.route("/start_genetic_algorithm", methods=['GET'])
def start_algorithm():
    @after_this_request
    def add_header(response):
        response.headers.add('Access-Control-Allow-Origin', '*')
        return response

    # Two arrays that will be returned as the response
    max_evolution = []
    mean_evolution = []

    # Get the parameters from the URL
    population_size = int(request.args.get('population'))
    left_closure, right_closure = int(request.args.get('left_closure')), int(request.args.get('right_closure'))
    a, b, c = int(request.args.get('a')), int(request.args.get('b')), int(request.args.get('c'))
    precision = int(request.args.get('precision'))
    prob_recombination = int(request.args.get('prob_recombination')) / 100
    prob_mutation = int(request.args.get('prob_mutation')) / 100
    steps = int(request.args.get('num_of_steps'))

    # First check if the parameters are valid, and if they are not,
    # return an empty response
    if not (population_size >= 1 and precision >= 1 and right_closure > left_closure and 0 <= prob_recombination <= 1 and 0 <= prob_mutation <= 1 and steps >= 1):
        return json.dumps({"max_evolution": max_evolution, "mean_evolution": mean_evolution })

    population = Population(population_size, left_closure, right_closure, a, b, c, precision)
    codif = Codification(left_closure, right_closure, precision)
    select = Selection(a, b, c)

    ##################################
    ########## First batch ###########
    ##################################

    # generate the first population randomly
    population.generate_all_chromosomes(codif)
    # generate all the fitness measurement
    select.generate_fitness_for_population(population.chromosomes_values)

    # generate probabilities
    select.generate_fitness_probabilities()
    # generate probability interval
    select.generate_fitness_intervals()

    # generate new chromosomes based on fitness value
    new_chromosomes_index = select.generate_chromosomes()
    population.transform_chromosomes(codif, new_chromosomes_index)
    select.generate_fitness_for_population(population.chromosomes_values)

    # define recombination and find which chromosomes to recombine
    recombination = Recombination(population.chromosomes, population.chromosomes_values, prob_recombination,
                                  codif.num_of_characteristics)
    chromosomes_to_recombine = recombination.generate_chromosomes_to_recombine()
    recombination.recombine_chromosomes(codif, chromosomes_to_recombine)
    population.chromosomes, population.chromosomes_values = recombination.chromosomes, recombination.chromosome_values
    select.generate_fitness_for_population(population.chromosomes_values)

    # define mutation and find which chromosomes to mutate
    mutation = Mutation(population.chromosomes, population.chromosomes_values, prob_mutation,
                        codif.num_of_characteristics)
    chromosomes_to_mutate = mutation.generate_chromosomes_to_mutate()
    mutation.mutate_chromosomes(codif, chromosomes_to_mutate)

    population.chromosomes, population.chromosomes_values = mutation.chromosomes, mutation.chromosome_values
    select.generate_fitness_for_population(population.chromosomes_values)

    print("Etapa 1: ", end="")
    max_step_value, mean_step_value = select.generate_fitness_statistics_print()
    max_evolution.append(max_step_value), mean_evolution.append(mean_step_value)

    for step in range(steps - 1):
        print(f"Etapa {step + 2}: ", end="")
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
        max_step_value, mean_step_value = select.generate_fitness_statistics_print()
        max_evolution.append(max_step_value), mean_evolution.append(mean_step_value)

    response = {"max_evolution": max_evolution, "mean_evolution": mean_evolution }

    return json.dumps(response)