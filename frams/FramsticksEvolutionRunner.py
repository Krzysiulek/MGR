import argparse
import sys

import FramsticksDiploidEvolution as diploid
import FramsticksHaploidEvolution as haploid
from FramsticksEvolutionCommon import parseArguments

DETERMINISTIC = False

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Run this program with "python -u %s" if you want to disable buffering of its output.' % sys.argv[0])
    parsed_args = parseArguments(parser=parser)
    print("Argument values:", ", ".join(['%s=%s' % (arg, getattr(parsed_args, arg)) for arg in vars(parsed_args)]))

    print(f"Running diploid")
    max_diploid = diploid.run(parsed_args=parsed_args, deterministic=DETERMINISTIC)
    print(f"Running haploid")
    max_haploid = haploid.run(parsed_args=parsed_args, deterministic=DETERMINISTIC)
    print(f"Max haploid = {max_haploid}. Max diploid = {max_diploid}")
