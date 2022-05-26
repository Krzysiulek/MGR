import argparse
import sys
import threading
import time

import FramsticksDiploidEvolution as diploid
import FramsticksHaploidEvolution as haploid
from FramsticksEvolutionCommon import parseArguments

from datetime import datetime


DETERMINISTIC = False
MAX_ITERS = None
MIN_ITERS = None

class myThread (threading.Thread):

   def __init__(self):
      threading.Thread.__init__(self)

   def run(self):



def print_time(type, max, time, iterations):
    print(f"[{type}] Max={max}. Took={time}. Iterations={iterations}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description='Run this program with "python -u %s" if you want to disable buffering of its output.' % sys.argv[
            0])
    parsed_args = parseArguments(parser=parser)
    print("Argument values:", ", ".join(['%s=%s' % (arg, getattr(parsed_args, arg)) for arg in vars(parsed_args)]))

    print(f"Running diploid")
    experiment_start_time = datetime.now()
    start = time.time()
    max_diploid, diploid_iters = diploid.run(parsed_args=parsed_args,
                                             deterministic=DETERMINISTIC,
                                             max_iters_limit=MAX_ITERS,
                                             min_iters_limit=MIN_ITERS,
                                             experiment_start_time=experiment_start_time)
    diploid_took = time.time() - start

    print(f"Running haploid")
    start = time.time()
    max_haploid, haploid_iters = haploid.run(parsed_args=parsed_args,
                                             deterministic=DETERMINISTIC,
                                             max_iters_limit=MAX_ITERS,
                                             min_iters_limit=MIN_ITERS,
                                             experiment_start_time=experiment_start_time)

    thread.start_new_thread(print_time, ("Thread-1", 2,))
    thread.start_new_thread(print_time, ("Thread-2", 4,))

    haploid_took = time.time() - start

    print_time("Haploid", max_haploid, haploid_took, haploid_iters)
    print_time("Diploid", max_diploid, diploid_took, diploid_iters)
