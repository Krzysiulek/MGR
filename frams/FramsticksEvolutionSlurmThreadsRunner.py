import argparse
import queue
import sys
import threading
import time
from multiprocessing import Process

import FramsticksDiploidEvolution as diploid
import FramsticksHaploidEvolution as haploid
from FramsticksEvolutionCommon import parseArguments

DETERMINISTIC = False
MAX_ITERS = 100
MIN_ITERS = 100


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


def worker():
    while True:
        item = q.get()
        item.start()
        item.join()
        q.task_done()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description='Run this program with "python -u %s" if you want to disable buffering of its output.' % sys.argv[
            0])
    parsed_args = parseArguments(parser=parser)
    print("Argument values:", ", ".join(['%s=%s' % (arg, getattr(parsed_args, arg)) for arg in vars(parsed_args)]))

    p_cross = 0.2
    p_mut = 0.9

    q = queue.Queue()

    # Turn-on the worker thread.
    threading.Thread(target=worker, daemon=True).start()

    for p_cross in [0.2]:
        for p_mut in [0.9]:
            experiments_num = 10
            for i in range(experiments_num):
                h = Process(target=haploid_function, args=(parsed_args, p_cross, p_mut))
                d = Process(target=diploid_function, args=(parsed_args, p_cross, p_mut))

                q.put(d)
                q.put(h)

    q.join()
