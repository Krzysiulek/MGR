import argparse
import sys
import time
from datetime import datetime
from multiprocessing import Process

import FramsticksDiploidEvolution as diploid
import FramsticksHaploidEvolution as haploid
from FramsticksEvolutionCommon import parseArguments

DETERMINISTIC = False
MAX_ITERS = 100
MIN_ITERS = None


def haploid_function(parsed_args, experiment_start_time, p_cx, p_mut):
    start = time.time()
    max_haploid, haploid_iters = haploid.run(parsed_args=parsed_args,
                                             deterministic=DETERMINISTIC,
                                             max_iters_limit=MAX_ITERS,
                                             min_iters_limit=MIN_ITERS,
                                             experiment_start_time=experiment_start_time,
                                             p_cx=p_cx,
                                             p_mut=p_mut)

    haploid_took = time.time() - start


def print_time(type, max, time, iterations):
    print(f"[{type}] Max={max}. Took={time}. Iterations={iterations}")


def diploid_function(parsed_args, experiment_start_time, p_cx, p_mut):
    start = time.time()
    max_diploid, diploid_iters = diploid.run(parsed_args=parsed_args,
                                             deterministic=DETERMINISTIC,
                                             max_iters_limit=MAX_ITERS,
                                             min_iters_limit=MIN_ITERS,
                                             experiment_start_time=experiment_start_time,
                                             p_cx=p_cx,
                                             p_mut=p_mut)
    diploid_took = time.time() - start


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description='Run this program with "python -u %s" if you want to disable buffering of its output.' % sys.argv[
            0])
    parsed_args = parseArguments(parser=parser)
    print("Argument values:", ", ".join(['%s=%s' % (arg, getattr(parsed_args, arg)) for arg in vars(parsed_args)]))

    # experiment_start_time = datetime.now()

    # p_cx = parsed_args.pxov
    # p_mut = parsed_args.pmut

    # h = Process(target=haploid_function, args=(parsed_args, experiment_start_time, p_cx, p_mut))
    # d = Process(target=diploid_function, args=(parsed_args, experiment_start_time, p_cx, p_mut))
    #
    # h.start()
    # d.start()
    #
    # h.join()
    # d.join()

    for p_cross in [1, 0.8, 0.6, 0.4, 0.2, 0.1, 0.05, 0.01]:
        for p_mut in [1, 0.8, 0.6, 0.4, 0.2, 0.1, 0.05, 0.01]:
            if (p_cross == 1 and p_mut == 1) or (p_cross == 1 and p_mut == 0.8):
                continue

            if p_mut > 0.4 or p_cross > 0.4:
                MAX_ITERS = 40
            else:
                MAX_ITERS = 300

            experiments_num = 3
            for i in range(experiments_num):
                print(f"DOING EXPERIMENT [{i}/{experiments_num}]: p_cx={p_cross}; p_mut={p_mut}")
                experiment_start_time = datetime.now()

                h = Process(target=haploid_function, args=(parsed_args, experiment_start_time, p_cross, p_mut))
                d = Process(target=diploid_function, args=(parsed_args, experiment_start_time, p_cross, p_mut))

                h.start()
                d.start()

                h.join()
                d.join()


# TODO zmiejszanie prawd. mutacji i krzyżowania co iteracje - eksperyment