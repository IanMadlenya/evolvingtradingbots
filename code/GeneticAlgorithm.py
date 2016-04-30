"""
    # for each day:
    # Generate N random individuals (or start from previous day's survivors)
    # for G generations:
    #   evaluate performance (fitness)
    #   those with high fitness can reproduce (crossover)
    #   apply random mutations to children

-For GA what is a better fitness function
--pure profit
--Sharpe's ratio
--number of wins
"""
from MRSingleDay import MRSingleDay
from FileIndexer import FileIndexer
import numpy as np
from datetime import datetime


NUM_GENERATIONS = 5
POP_SIZE = 6  # population size
SURVIVAL_RATE = 0.5
MUTATION_RATE = 0.4

PROFIT_TARGET = 2
STOP_LOSS = -5

def crossover(ina, inb):
    """Returns a crossover pair of ina and inb"""
    return [(ina[0], inb[1]), (inb[0], ina[1])]


def mutate(in_tup):
    """ Code borrowed from this project's SimulatedAnnealing modifyParameters"""
    mod_scaling_parameter = np.max((in_tup[0] + np.random.normal()), 0.1)
    mod_mean_days = np.maximum((in_tup[1] + np.random.randint(-1, 2)), 1)
    return (mod_scaling_parameter, mod_mean_days)


def reproduce_mutate(sorted_fitness, solutions):
    """allows the fittest to reproduce, also applies mutation"""
    ret_solns = []
    # those with high fitness can reproduce (crossover)
    print sorted_fitness
    reproducing_size = int(POP_SIZE * SURVIVAL_RATE)
    index = 0
    for k in range(reproducing_size):
        for j in range(k, reproducing_size):
            if k != j:
                gene_a = solutions[sorted_fitness[k]]
                gene_b = solutions[sorted_fitness[j]]
                ret_solns.extend(crossover(gene_a, gene_b))

    # apply random mutations to children
    mutation_rvs = np.random.uniform(0, 1, POP_SIZE)
    for m in np.flatnonzero(mutation_rvs < MUTATION_RATE):
        print "mutation happended!"
        ret_solns[m] = mutate(ret_solns[m])

    return ret_solns


def single_period_ga(fn, solns, fitness_ftn):
    """Perform genetic algorithm for a single day"""
    best_soln = None
    best_fitness = float('-inf')
    for g in range(NUM_GENERATIONS):
        print "generation: ",g
        fitness = np.zeros(POP_SIZE)
        for i, sol in enumerate(solns):# iterate over all the members of the population
            # evaluate performance (fitness)
            d = MRSingleDay(fn, sol[0], sol[1], PROFIT_TARGET, STOP_LOSS)
            ro = d.calc_returns()
            fitness[i] = fitness_ftn(ro)
            print sol, i, fitness[i]
        sorted_fitness = np.argsort(fitness)[::-1]

        if fitness[sorted_fitness[0]] > best_fitness:  # find the best solution
            best_fitness = fitness[sorted_fitness[0]]
            best_soln = solns[sorted_fitness[0]]

        solns = reproduce_mutate(sorted_fitness, solns)

    return best_fitness, best_soln, solns


def init_solns():
    return [(2.033, 3), (-2.397, 5), (-0.940, 7), (-1.563, 4), (2.067, 9), (0.817, 2)]

def cum_ret_fitness(ro_in):
    """Returns the cumulative returns from a trade result object"""
    return ro_in.cum_ret

if __name__ == '__main__':
    fIndexer = FileIndexer("../data/min/")
    fileList = fIndexer.getFilesForPeriod(datetime(2014, 4, 1), datetime(2016, 1, 1))

    i = 0
    survivors = init_solns()
    fw = open("GA_results.txt", 'w')
    for i in np.arange(fileList.shape[0]):     # for each day:
        p_best_fit, p_best_soln, survivors = single_period_ga(fileList[i], survivors, cum_ret_fitness)
        # run best soln on next day (out of sample testing)
        d = MRSingleDay(fileList[i+1], p_best_soln[0], p_best_soln[1], PROFIT_TARGET, STOP_LOSS)
        ro = d.calc_returns()
        fw.write("{}\t{}\t{}\t{}\t{}\n".format(fileList[i], p_best_fit, p_best_soln[0], p_best_soln[1], ro.cum_ret))

    fw.close()
    print "all done"
