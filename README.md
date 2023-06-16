# GeneticAlgorithmMaximumOfFunction
Maximizing a quadric positive function using a genetic algorithm by following the next steps:

_NOTATIONS:_ <br/>
**S** = number of steps <br/>
**PR** = probability of recombination <br/>
**PM** = probability of mutation <br/>

1. **Initialize population**: initialize a population of N chromosomes by randomly selecting a number inside the definition domain of the function and finding its placement inside the discretization intervals
2. **Selection**: Choose the parent chromosomes for the next generation, depending on the value of the fitness function
3. **Crossover**: Randomly generate a number between _[0,1]_ for each chromosome, and if it is **> PR**, than the current chromosome will be recombined. Afterward, randomly choose 2 chromosomes from the list of chromosomes to be recombined, and recombine them.
4. **Mutation**: Analogously choose chromosomes to mutate, but this time compares the random number with **PM**. For each chromosome, modify the same gene: chromosome[gene] = !chromosome[gene] ( from 0 --> 1, and from 1 --> 0)
5. **Evaluation**: Evaluate the current generation by calculating the maximum value of the fitness function & the mean value of the fitness function for the whole generation

Repeat steps 2,3,4,5 **S** times.

## How to run the code:
- activate the virtual env: _./venv/Scripts/activate_
- run the flask server: _../backend> flask run_
- open _../user-interface/index.html_ in a Web browser
