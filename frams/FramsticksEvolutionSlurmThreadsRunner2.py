import argparse
import queue
import sys
import threading
from datetime import datetime
from multiprocessing import Process

import FramsticksDiploidEvolution as diploid
import FramsticksHaploidEvolution as haploid
import os
from FramsticksEvolutionCommon import parseArguments

DETERMINISTIC = False
MAX_ITERS = None
MIN_ITERS = None


# <state>_<pop_made>_<type>_<time_updated>.json

def get_all_files_in_dir(dir):
    files = []
    for file_name in os.listdir(dir):
        if file_name.__contains__('ready'):
            files.append(file_name)

    return sorted(files, key=sorter)

def sorter(item):
    return item.split("_")[1]

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description='Run this program with "python -u %s" if you want to disable buffering of its output.' % sys.argv[
            0])
    parsed_args = parseArguments(parser=parser)
    # setattr(parsed_args, 'hof_size', 'test')
    print("Argument values:", ", ".join(['%s=%s' % (arg, getattr(parsed_args, arg)) for arg in vars(parsed_args)]))

    rootdir = "jobs"
    files = get_all_files_in_dir(rootdir)
    print(files)

    file_to_work_with = files[0]
    splited_file_to_work_with = file_to_work_with.split("_")
    splited_file_to_work_with[0] = "locked"
    splited_file_to_work_with[3] = str(datetime.now())

    new_name = "_".join(splited_file_to_work_with)
    os.rename(f"{rootdir}/{file_to_work_with}", f"{rootdir}/{new_name}")

