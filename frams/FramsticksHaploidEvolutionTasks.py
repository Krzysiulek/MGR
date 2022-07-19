import argparse
import random
import sys
import time

import numpy as np
from deap import creator, tools, base

# do modyfikacji. Wzięte z deap'a
from FramsticksEvolutionCommon import genotype_within_constraint, parseArguments, get_seed, save_logs, \
    append_logs, get_time_from_start, get_type
from FramsticksLib import FramsticksLib
from mydeap import algorithms


def frams_evaluate(frams_cli, OPTIMIZATION_CRITERIA, parsed_args, individual):
    BAD_FITNESS = [-1] * len(
        OPTIMIZATION_CRITERIA)  # fitness of -1 is intended to discourage further propagation of this genotype via selection ("this genotype is very poor")
    genotype = individual[
        0]  # individual[0] because we can't (?) have a simple str as a deap genotype/individual, only list of str.
    data = frams_cli.evaluate([genotype])
    # print("Evaluated '%s'" % genotype, 'evaluation is:', data)
    valid = True
    try:
        first_genotype_data = data[0]
        evaluation_data = first_genotype_data["evaluations"]
        default_evaluation_data = evaluation_data[""]
        fitness = [default_evaluation_data[crit] for crit in OPTIMIZATION_CRITERIA]
    except (KeyError,
            TypeError) as e:  # the evaluation may have failed for an invalid genotype (such as X[@][@] with "Don't simulate genotypes with warnings" option) or for some other reason
        valid = False
        print('Problem "%s" so could not evaluate genotype "%s", hence assigned it low fitness: %s' % (
            str(e), genotype, BAD_FITNESS))
    if valid:
        default_evaluation_data['numgenocharacters'] = len(genotype)  # for consistent constraint checking below
        valid &= genotype_within_constraint(genotype, default_evaluation_data, 'numparts', parsed_args.max_numparts)
        valid &= genotype_within_constraint(genotype, default_evaluation_data, 'numjoints', parsed_args.max_numjoints)
        valid &= genotype_within_constraint(genotype, default_evaluation_data, 'numneurons', parsed_args.max_numneurons)
        valid &= genotype_within_constraint(genotype, default_evaluation_data, 'numconnections',
                                            parsed_args.max_numconnections)
        valid &= genotype_within_constraint(genotype, default_evaluation_data, 'numgenocharacters',
                                            parsed_args.max_numgenochars)
    if not valid:
        fitness = BAD_FITNESS
    return fitness


def frams_crossover(frams_cli, individual1, individual2):
    geno1 = individual1[
        0]  # individual[0] because we can't (?) have a simple str as a deap genotype/individual, only list of str.
    geno2 = individual2[
        0]  # individual[0] because we can't (?) have a simple str as a deap genotype/individual, only list of str.
    individual1[0] = frams_cli.crossOver(geno1, geno2)
    individual2[0] = frams_cli.crossOver(geno1, geno2)
    return individual1, individual2


def frams_mutate(frams_cli, individual):
    individual[0] = frams_cli.mutate([individual[0]])[
        0]  # individual[0] because we can't (?) have a simple str as a deap genotype/individual, only list of str.
    return individual


def frams_getsimplest(frams_cli, genetic_format, initial_genotype):
    return initial_genotype if initial_genotype is not None else frams_cli.getSimplest(genetic_format)


def prepareToolbox(frams_cli, tournament_size, genetic_format, initial_genotype, OPTIMIZATION_CRITERIA, parsed_args):
    creator.create("FitnessMax", base.Fitness, weights=[1.0] * len(OPTIMIZATION_CRITERIA))
    creator.create("Individual", list,
                   fitness=creator.FitnessMax)  # would be nice to have "str" instead of unnecessary "list of str"

    toolbox = base.Toolbox()
    toolbox.register("attr_simplest_genotype", frams_getsimplest, frams_cli, genetic_format,
                     initial_genotype)  # "Attribute generator"
    toolbox.register("individual", tools.initRepeat, creator.Individual, toolbox.attr_simplest_genotype, 1)
    toolbox.register("population", tools.initRepeat, list, toolbox.individual)
    toolbox.register("evaluate", frams_evaluate, frams_cli, OPTIMIZATION_CRITERIA, parsed_args)
    toolbox.register("mate", frams_crossover, frams_cli)
    toolbox.register("mutate", frams_mutate, frams_cli)
    if len(OPTIMIZATION_CRITERIA) <= 1:
        toolbox.register("select", tools.selTournament, tournsize=tournament_size)
    else:
        toolbox.register("select", tools.selNSGA2)
    return toolbox


def print_best_individuals(hof):
    print('Best individuals:')
    for ind in hof:
        print(ind.fitness, '\t-->\t', ind[0])


def run(parsed_args,
        deterministic=False,
        experiment_start_time=None,
        p_mut=1,
        p_cx=1,
        log=None,
        hof=None,
        pop=None):
    random.seed(get_seed(deterministic))
    FramsticksLib.DETERMINISTIC = deterministic

    OPTIMIZATION_CRITERIA = parsed_args.opt.split(",")
    framsLib = FramsticksLib(parsed_args.path, parsed_args.lib, parsed_args.sim.split(";"))

    toolbox = prepareToolbox(framsLib, parsed_args.tournament,
                             '1' if parsed_args.genformat is None else parsed_args.genformat,
                             parsed_args.initialgenotype,
                             OPTIMIZATION_CRITERIA=OPTIMIZATION_CRITERIA,
                             parsed_args=parsed_args)
    if log == "" or log == None:
        log = []

    if pop == "" or pop == None:
        pop = toolbox.population(n=parsed_args.popsize)

    if hof == "" or hof == None:
        hof = tools.HallOfFame(parsed_args.hof_size)

    stats = tools.Statistics(lambda ind: ind.fitness.values)
    stats.register("type", get_type, 'H')
    stats.register("avg", np.mean)
    stats.register("stddev", np.std)
    stats.register("min", np.min)
    stats.register("max", np.max)
    stats.register("time", get_time_from_start, log, time.time())

    pop, tmp_log = algorithms.eaSimple(population=pop,
                                       toolbox=toolbox,
                                       cxpb=p_cx,
                                       mutpb=p_mut,
                                       ngen=parsed_args.generations,
                                       stats=stats,
                                       halloffame=hof,
                                       verbose=True)
    log = append_logs(log, tmp_log)


    save_logs(log=log,
              popsize=parsed_args.popsize,
              type="Haploid",
              hof=hof,
              optimization_criteria=OPTIMIZATION_CRITERIA,
              experiment_start_time=experiment_start_time,
              p_mut=p_mut,
              p_cx=p_cx,
              initial_genotype=parsed_args.initialgenotype,
              sim=parsed_args.sim,
              max_numgenochars=parsed_args.max_numgenochars,
              max_numparts=parsed_args.max_numparts,
              framsLib=framsLib)

    print_best_individuals(hof)

    return log, hof, pop


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description='Run this program with "python -u %s" if you want to disable buffering of its output.' % sys.argv[
            0])
    parsed_args = parseArguments(parser=parser)
    print("Argument values:", ", ".join(['%s=%s' % (arg, getattr(parsed_args, arg)) for arg in vars(parsed_args)]))

    run(parsed_args=parsed_args)
