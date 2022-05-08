import os
import json
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


def ensureDir(string):
    if os.path.isdir(string):
        return string
    else:
        raise NotADirectoryError(string)


def get_seed(deterministic):
    return 123 if deterministic else None

def get_metadata(pop_size):
    return {
        "type": "haploid",
        "population_size": pop_size
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

def save_logs(log, popsize):
    dict_to_save = {}
    dict_to_save["metadata"] = get_metadata(pop_size=popsize)
    dict_to_save["logs"] = get_population_logs(log, popsize)

    now = datetime.now().strftime("%d-%m-%Y-%H-%M-%S")
    with open(f'data/train_{now}.json', 'w') as fout:
        json.dump(dict_to_save, fout)


def has_reached_iters_limits(limit, current_iter):
    if limit is None:
        return False

    return current_iter >= limit


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
    return parser.parse_args()
