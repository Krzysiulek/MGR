import json
import os
import random
import time
from datetime import datetime


def genotype_within_constraint(genotype, dict_criteria_values, criterion_name, constraint_value):
    REPORT_CONSTRAINT_VIOLATIONS = False
    if constraint_value is not None:
        actual_value = dict_criteria_values[criterion_name]
        if actual_value > constraint_value:
            if REPORT_CONSTRAINT_VIOLATIONS:
                print(
                    'Genotype "%s" assigned low fitness because it violates constraint "%s": %s exceeds threshold %s' % (
                        genotype, criterion_name, actual_value, constraint_value))
            return False
    return True


def reproduce_hof(hof, population):
    if len(hof) <= 0:
        return population

    changed = 0

    random_genes_to_change = random.sample(range(0, len(population) - 1), int(len(population) / 5))

    for i in random_genes_to_change:
        population[i] = hof.items[0]

    for i in range(int(len(population))):
        ind = population[i]

        if max(ind.fitness.values) < get_max_in_hof(hof) / 2:
            population[i] = hof.items[0]

    return population


def ensureDir(string):
    if os.path.isdir(string):
        return string
    else:
        raise NotADirectoryError(string)


def get_time_from_start(logs, passed_time, arg2):
    # logs = []
    if len(logs) > 0:
        return time.time() - passed_time + logs[-1]["time"]

    return time.time() - passed_time


def get_type(type, arg):
    return type


def append_logs(logs, logs_to_append):
    if len(logs) > 0:
        max_gen = logs[len(logs) - 1]["gen"]
    else:
        max_gen = 0

    for log in logs_to_append:
        max_gen += 1
        log["gen"] = max_gen
        logs.append(log)

    return logs


def get_seed(deterministic):
    return 123 if deterministic else None


def get_hof_info(hof, optimization_criteria):
    keyval_list = []
    for ind in hof:
        keyval = {}

        for i, k in enumerate(optimization_criteria):  # construct a dictionary with criteria names and their values
            # TODO it would be better to save in Individual (after evaluation) all fields returned by Framsticks, and get these fields here, not just the criteria that were actually used as fitness in evolution.
            keyval[k] = ind.fitness.values[i]

        keyval["genotype"] = ind
        keyval_list.append(keyval)
    return keyval_list


def get_max_in_hof(hof):
    max_hof = 0
    for ind in hof:
        if max_hof < max(ind.fitness.values):
            max_hof = max(ind.fitness.values)
    return max_hof

def get_hof_additional_informations(framsLib, hof):
    if framsLib is None:
        return []

    properties = []

    for item in hof.items[0]:
        properties.append(framsLib.evaluate([item])[0]['evaluations'][''])

    return properties


def get_metadata(pop_size=0,
                 type="",
                 hof=None,
                 optimization_criteria=None,
                 p_mut=None,
                 p_cx=None,
                 initial_genotype="",
                 sim="",
                 max_numgenochars=None,
                 max_numparts=None,
                 framsLib=None):
    return {
        "type": type,
        "population_size": pop_size,
        "hof": get_hof_info(hof=hof, optimization_criteria=optimization_criteria),
        "p_mut": p_mut,
        "p_cx": p_cx,
        "initial_genotype": initial_genotype,
        "sim": sim,
        "max_numgenochars": max_numgenochars,
        "max_numparts": max_numparts,
        "hof_all_properties": get_hof_additional_informations(framsLib=framsLib, hof=hof)
    }


def get_population_logs(log, popsize):
    trained_pop_num = 0
    list_to_save = []

    hof = -99
    for i in range(len(log)):
        trained_pop_num += popsize
        dict_log = log[i]
        dict_log['trained_pop'] = trained_pop_num

        if dict_log['max'] > hof:
            hof = dict_log['max']

        dict_log['hof_fitness'] = hof

        list_to_save.append(dict_log)

    return list_to_save


def save_logs(log,
              popsize,
              type="",
              hof=None,
              optimization_criteria=None,
              experiment_start_time=datetime.now(),
              p_mut=None,
              p_cx=None,
              initial_genotype=None,
              sim=None,
              max_numgenochars=None,
              max_numparts=None,
              framsLib=None
              ):
    dict_to_save = {}
    dict_to_save["metadata"] = get_metadata(pop_size=popsize,
                                            type=type,
                                            hof=hof,
                                            optimization_criteria=optimization_criteria,
                                            p_mut=p_mut,
                                            p_cx=p_cx,
                                            initial_genotype=initial_genotype,
                                            sim=sim,
                                            max_numgenochars=max_numgenochars,
                                            max_numparts=max_numparts,
                                            framsLib=framsLib)
    dict_to_save["logs"] = get_population_logs(log, popsize)

    if isinstance(experiment_start_time, str):
        now = experiment_start_time
    else:
        now = experiment_start_time.strftime("%d-%m-%Y-%H-%M-%S.%f")

    opt_criterias = str("_".join(optimization_criteria))
    dir = f'data/{opt_criterias}_pcx_{p_cx}_pmut_{p_mut}_popsize_{popsize}'
    path = f'{dir}/train_{now}_{type}_pcx_{p_cx}_pmut_{p_mut}.json'

    for i in range(100):
        try:
            os.makedirs(dir, exist_ok=True)
            with open(path, 'w') as fout:
                json.dump(dict_to_save, fout)
            print(f"Saved file  with [{i}] try. File=[{path}]")
            break

        except Exception:
            print(f"Try: {i}. Exception while saving file {path}")
            time.sleep(2)


def has_reached_iters_limits(limit, current_iter):
    if limit is None:
        return False

    return current_iter >= limit


def should_continue_simulation(current_iter, max_limit, min_limit, is_improving):
    if min_limit is not None and min_limit > current_iter:
        return True

    if max_limit is not None and current_iter >= max_limit:
        return False

    return is_improving


def parseArguments(parser, canSkipRequired=False):
    parser.add_argument('-path', type=ensureDir, required=True and canSkipRequired,
                        help='Path to Framsticks CLI without trailing slash.')
    parser.add_argument('-lib', required=False,
                        help='Library name. If not given, "frams-objects.dll" or "frams-objects.so" is assumed depending on the platform.')
    parser.add_argument('-sim', required=False, default="eval-allcriteria.sim",
                        help="The name of the .sim file with settings for evaluation, mutation, crossover, and similarity estimation. If not given, \"eval-allcriteria.sim\" is assumed by default. Must be compatible with the \"standard-eval\" expdef. If you want to provide more files, separate them with a semicolon ';'.")

    parser.add_argument('-genformat', required=False,
                        help='Genetic format for the simplest initial genotype, for example 4, 9, or B. If not given, f1 is assumed.')
    parser.add_argument('-initialgenotype', required=False,
                        help='The genotype used to seed the initial population. If given, the -genformat argument is ignored.')

    parser.add_argument('-opt', required=True and canSkipRequired,
                        help='optimization criteria: vertpos, velocity, distance, vertvel, lifespan, numjoints, numparts, numneurons, numconnections (or other as long as it is provided by the .sim file and its .expdef). For multiple criteria optimization, separate the names by the comma.')
    parser.add_argument('-popsize', type=int, default=50, help="Population size, default: 50.")
    parser.add_argument('-generations', type=int, default=5, help="Number of generations, default: 5.")
    parser.add_argument('-tournament', type=int, default=5, help="Tournament size, default: 5.")
    parser.add_argument('-pmut', type=float, default=0.9, help="Probability of mutation, default: 0.9")
    parser.add_argument('-pxov', type=float, default=0.2, help="Probability of crossover, default: 0.2")
    parser.add_argument('-hof_size', type=int, default=10, help="Number of genotypes in Hall of Fame. Default: 10.")
    parser.add_argument('-hof_savefile', required=False,
                        help='If set, Hall of Fame will be saved in Framsticks file format (recommended extension *.gen).')

    parser.add_argument('-max_numparts', type=int, default=None, help="Maximum number of Parts. Default: no limit")
    parser.add_argument('-max_numjoints', type=int, default=None, help="Maximum number of Joints. Default: no limit")
    parser.add_argument('-max_numneurons', type=int, default=None, help="Maximum number of Neurons. Default: no limit")
    parser.add_argument('-max_numconnections', type=int, default=None,
                        help="Maximum number of Neural connections. Default: no limit")
    parser.add_argument('-max_numgenochars', type=int, default=None,
                        help="Maximum number of characters in genotype (including the format prefix, if any). Default: no limit")
    parser.add_argument('-iters', type=int, default=None, help="Ile iteracji algorytmu ma sie zrobi?? ")

    parser.add_argument('-task', type=str, default=None,
                        help="haploid or diploid")
    return parser.parse_args()
