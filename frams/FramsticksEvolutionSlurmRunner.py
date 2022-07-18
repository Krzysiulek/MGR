import argparse
import sys
from datetime import datetime

import FramsticksDiploidEvolution as diploid
import FramsticksHaploidEvolution as haploid
from FramsticksEvolutionCommon import parseArguments

DETERMINISTIC = False


def haploid_function(parsed_args, p_cx, p_mut, iters):
    experiment_start_time = datetime.now()
    haploid.run(parsed_args=parsed_args,
                deterministic=DETERMINISTIC,
                max_iters_limit=iters,
                min_iters_limit=iters,
                experiment_start_time=experiment_start_time,
                p_cx=p_cx,
                p_mut=p_mut)


def diploid_function(parsed_args, p_cx, p_mut, iters):
    experiment_start_time = datetime.now()
    diploid.run(parsed_args=parsed_args,
                deterministic=DETERMINISTIC,
                max_iters_limit=iters,
                min_iters_limit=iters,
                experiment_start_time=experiment_start_time,
                p_cx=p_cx,
                p_mut=p_mut)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description='Run this program with "python -u %s" if you want to disable buffering of its output.' % sys.argv[
            0])
    parsed_args = parseArguments(parser=parser)
    print("Argument values:", ", ".join(['%s=%s' % (arg, getattr(parsed_args, arg)) for arg in vars(parsed_args)]))

    p_cross = 0.2
    p_mut = 0.9

    task = parsed_args.task
    iters = parsed_args.iters

    if task == "haploid":
        haploid_function(parsed_args, p_cross, p_mut, iters)
    elif task == "diploid":
        diploid_function(parsed_args, p_cross, p_mut, iters)
