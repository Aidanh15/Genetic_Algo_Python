# Aidan Hanley, 24/05/20.
# List of varible descriptions for the program to breed a large rat from a subset population of smaller rats:
# GOAL = 50000   --> target weight of bred rat in grams
# NUM_RATS = 20  --> total num of adult rats supported
# INITIAL_MIN_WT = 200 --> minimum weight of adult rat in grams in initial population
# INITIAL_MAX_WT = 600 --> maximum weight of adult rat in grams in initial population
# INITIAL_MODE_WT = 300 --> most common adult rat weight in grams in initial population
# MUTATE_ODDS = 0.01 --> probability of mutation occurring in a rat
# MUTATE_MIN = 0.5 --> scalar on rat weight of least beneficial mutation
# MUTATE_MAX = 1.2 --> scalar on rat weight of most beneficial mutation
# LITTER_SIZE = 8 num of pups per pair of mating rats
# LITTERS_PER_YEAR = 10  num of litters per year per pair of mating rats
# GENERATION_LIMIT = 500 generational cutoff to stop breeding program
# life span is not accounted for, assume quick culling of parent rats

import time  #record runtime of G.A
import random 
import statistics  #get mean etc 

# CONSTANTS - weights in grams
GOAL = 50000 
NUM_RATS = 20
INITIAL_MIN_WT = 200
INITIAL_MAX_WT = 600 
INITIAL_MODE_WT = 300 
MUTATE_ODDS = 0.01
MUTATE_MIN = 0.5
MUTATE_MAX = 1.2
LITTER_SIZE = 8 
LITTERS_PER_YEAR = 10 
GENERATION_LIMIT = 500 

#Ensure even amounts of rats for breeding pair purposes:
if NUM_RATS % 2 != 0:
    NUM_RATS += 1


def populate(num_rats, min_wt, max_wt, mode_wt):
    """Initialise a population with a triangular distribution of weights:"""
    return [int(random.triangular(min_wt, max_wt, mode_wt))\
        for i in range(num_rats)]


def fitness(population, goal):
    """measure pop. fitness based on an attribute mean vs target:"""
    avg = statistics.mean(population)
    return avg/goal

def select(population, to_retain):
    """Cull a population to retain only a specified number of members."""
    sorted_population = sorted(population)
    to_retain_by_sex = to_retain//2
    members_per_sex = len(sorted_population)//2
    females = sorted_population[:members_per_sex]
    males = sorted_population[members_per_sex:]
    selected_females = females[- to_retain_by_sex:]
    selected_males = males[- to_retain_by_sex:]
    return selected_males, selected_females 

#Below is the def to breed the next generation. 
# A key assumption is that the weight of the offspring will be greater than or equal to the weight of the mother and <= the father.
#Exceptions will be handled in the mutation function.

def breed(males, females, litter_size):
    """Crossover genes among members (weights) of a population"""
    random.shuffle(males)
    random.shuffle(females)
    children = []
    for male, female in zip(males, females):
        for child in range(litter_size):
            child = random.randint(female, male)
            children.append(child)
    return children



def mutate(children, mutate_odds, mutate_min, mutate_max):
    """Randomly alter rat weights using input odds & fractional changes changes"""
    for index, rat in enumerate(children):
        if mutate_odds >= random.random():
            children[index] = round(rat * random.uniform(mutate_min, mutate_max))
    return children



def main():
    """Initialise population, select, breed and mutate, display results."""
    generations = 0    #initial num of generations

    parents = populate(NUM_RATS, INITIAL_MIN_WT, INITIAL_MAX_WT, INITIAL_MODE_WT)
    print("initial population weights: = {}".format(parents))

    popl_fitness = fitness(parents, GOAL)
    print ("Initial population fitness = {}".format(popl_fitness))
    print("Number to retain = {}".format(NUM_RATS))

    avg_wt = [] #avg weight of each generation

    while popl_fitness < 1 and generations < GENERATION_LIMIT:   #Stop conditions: reached target weight or max num of generations reached without hitting target wt
        selected_males, selected_females = select(parents, NUM_RATS)
        children = breed(selected_males, selected_females, LITTER_SIZE)
        children = mutate(children, MUTATE_ODDS, MUTATE_MIN, MUTATE_MAX)
        parents = selected_males + selected_females + children
        popl_fitness = fitness(parents, GOAL)
        print("Generation {} fitness = {:.4f}".format(generations, popl_fitness))
        avg_wt.append(int(statistics.mean(parents)))
        generations += 1
        print("Average weight per generation = {}".format(avg_wt))
        print("\nnumber of generations = {}".format(generations))
        print("Number of years = {}".format(int(generations / LITTERS_PER_YEAR)))

if __name__ == '__main__':
    start_time = time.time()
    main()
    end_time = time.time()
    duration = end_time - start_time
    print("\nRuntime for this program was {} seconds".format(duration))

# After running, will take 37.8 years to produce the optimally weighted offspring.
#How could this algo be optimised? : future work

