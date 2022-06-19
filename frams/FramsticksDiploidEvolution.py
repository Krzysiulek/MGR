import argparse
import random
import sys
import time

import numpy as np
from deap import creator, tools, base

# do modyfikacji. Wzięte z deap'a
from FramsticksEvolutionCommon import genotype_within_constraint, parseArguments, get_seed, save_logs, \
    should_continue_simulation, append_logs, get_max_in_hof, get_time_from_start, get_type
from FramsticksLib import FramsticksLib
from mydeap import algorithms


def calculate_fitness(frams_cli, genotype, OPTIMIZATION_CRITERIA, parsed_args):
    BAD_FITNESS = [-1] * len(
        OPTIMIZATION_CRITERIA)  # fitness of -1 is intended to discourage further propagation of this genotype via selection ("this genotype is very poor")
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


def frams_evaluate(frams_cli, OPTIMIZATION_CRITERIA, parsed_args, individual):
    genotype = individual[
        0]  # individual[0] because we can't (?) have a simple str as a deap genotype/individual, only list of str.

    fitness1 = calculate_fitness(frams_cli=frams_cli,
                                 genotype=individual[0],
                                 OPTIMIZATION_CRITERIA=OPTIMIZATION_CRITERIA,
                                 parsed_args=parsed_args)

    fitness2 = calculate_fitness(frams_cli=frams_cli,
                                 genotype=individual[1],
                                 OPTIMIZATION_CRITERIA=OPTIMIZATION_CRITERIA,
                                 parsed_args=parsed_args)

    return max(fitness1, fitness2)


def frams_crossover(frams_cli, individual1, individual2):
    geno1_1 = individual1[0]
    geno1_2 = individual1[1]

    geno2_1 = individual2[0]
    geno2_2 = individual2[1]

    candidates = []

    candidates.append(frams_cli.crossOver(geno1_1, geno2_1))
    candidates.append(frams_cli.crossOver(geno1_1, geno2_2))
    candidates.append(frams_cli.crossOver(geno1_2, geno2_1))
    candidates.append(frams_cli.crossOver(geno1_2, geno2_2))

    random.shuffle(candidates)

    individual1[0] = candidates[0]
    individual1[1] = candidates[1]
    individual2[0] = candidates[2]
    individual2[1] = candidates[3]

    return individual1, individual2


def frams_mutate(frams_cli, individual):
    individual[0] = frams_cli.mutate([individual[0]])[
        0]  # individual[0] because we can't (?) have a simple str as a deap genotype/individual, only list of str.
    individual[1] = frams_cli.mutate([individual[1]])[
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


def save_genotypes(filename, OPTIMIZATION_CRITERIA, hof):
    from framsfiles import writer as framswriter
    with open(filename, "w") as outfile:
        for ind in hof:
            keyval = {}
            for i, k in enumerate(OPTIMIZATION_CRITERIA):  # construct a dictionary with criteria names and their values
                keyval[k] = ind.fitness.values[
                    i]  # TODO it would be better to save in Individual (after evaluation) all fields returned by Framsticks, and get these fields here, not just the criteria that were actually used as fitness in evolution.
            # Note: prior to the release of Framsticks 5.0, saving e.g. numparts (i.e. P) without J,N,C breaks re-calcucation of P,J,N,C in Framsticks and they appear to be zero (nothing serious).
            outfile.write(framswriter.from_collection({"_classname": "org", "genotype": ind[0], **keyval}))
            outfile.write("\n")
    print("Saved '%s' (%d)" % (filename, len(hof)))


def print_best_individuals(hof):
    print('Best individuals:')
    for ind in hof:
        print(ind.fitness, '\t-->\t', ind[0])
        print(ind.fitness, '\t-->\t', ind[1])


def duplicateIndividuals(population):
    for individual in population:
        individual.append(individual[0])
    return population

def run(parsed_args,
        deterministic=False,
        max_iters_limit=None,
        min_iters_limit=None,
        experiment_start_time=None,
        p_mut=1,
        p_cx=1):
    random.seed(get_seed(deterministic))
    FramsticksLib.DETERMINISTIC = deterministic

    OPTIMIZATION_CRITERIA = parsed_args.opt.split(",")
    framsLib = FramsticksLib(parsed_args.path, parsed_args.lib, parsed_args.sim.split(";"))

    toolbox = prepareToolbox(framsLib, parsed_args.tournament,
                             '1' if parsed_args.genformat is None else parsed_args.genformat,
                             parsed_args.initialgenotype,
                             OPTIMIZATION_CRITERIA=OPTIMIZATION_CRITERIA,
                             parsed_args=parsed_args)

    pop = toolbox.population(n=parsed_args.popsize)
    pop = duplicateIndividuals(pop)

    hof = tools.HallOfFame(parsed_args.hof_size)
    stats = tools.Statistics(lambda ind: ind.fitness.values)
    stats.register("type", get_type, 'D')
    stats.register("avg", np.mean)
    stats.register("stddev", np.std)
    stats.register("min", np.min)
    stats.register("max", np.max)
    stats.register("time", get_time_from_start, time.time())

    hof_fitness = get_max_in_hof(hof)

    should_continue = True
    log = []
    iters = 0
    while (should_continue):
        # pop = reproduce_hof(hof=hof, population=pop)
        iters += 1
        print(f"Calculating Diploid. Iteration: {iters}")

        pop, tmp_log = algorithms.eaSimple(population=pop,
                                           toolbox=toolbox,
                                           cxpb=p_cx,
                                           mutpb=p_mut,
                                           # cxpb=parsed_args.pxov, mutpb=parsed_args.pmut,
                                           ngen=parsed_args.generations,
                                           stats=stats,
                                           halloffame=hof,
                                           verbose=True)
        log = append_logs(log, tmp_log)

        if (get_max_in_hof(hof) > hof_fitness):
            hof_fitness = get_max_in_hof(hof)
            print(f"Still improving. Max={get_max_in_hof(hof)}. Hof={hof}")
            print(hof)
            still_improving = True
        else:
            still_improving = False

        should_continue = should_continue_simulation(current_iter=iters * parsed_args.popsize * parsed_args.generations,
                                                     max_limit=max_iters_limit,
                                                     min_limit=min_iters_limit,
                                                     is_improving=still_improving)

        save_logs(log=log,
                  popsize=parsed_args.popsize,
                  type="Diploid",
                  hof=hof,
                  optimization_criteria=OPTIMIZATION_CRITERIA,
                  experiment_start_time=experiment_start_time,
                  p_mut=p_mut,
                  p_cx=p_cx,
                  initial_genotype=parsed_args.initialgenotype,
                  sim=parsed_args.sim,
                  max_numgenochars=parsed_args.max_numgenochars,
                  max_numparts=parsed_args.max_numparts)

    print_best_individuals(hof)

    if parsed_args.hof_savefile is not None:
        save_genotypes(parsed_args.hof_savefile, OPTIMIZATION_CRITERIA, hof)

    return get_max_in_hof(hof), iters


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description='Run this program with "python -u %s" if you want to disable buffering of its output.' % sys.argv[
            0])
    parsed_args = parseArguments(parser=parser)
    print("Argument values:", ", ".join(['%s=%s' % (arg, getattr(parsed_args, arg)) for arg in vars(parsed_args)]))

    run(parsed_args=parsed_args)
