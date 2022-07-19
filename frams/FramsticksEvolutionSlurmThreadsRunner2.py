import argparse
import json
import os
import sys
from datetime import datetime

import FramsticksDiploidEvolutionTasks as diploid
import FramsticksHaploidEvolutionTasks as haploid
from FramsticksEvolutionCommon import parseArguments
import time

DETERMINISTIC = False
MAX_ITERS = None
MIN_ITERS = None
import dill as pickle
from os.path import exists


def haploid_function(parsed_args, p_cx, p_mut, log, hof, pop, experiment_start_time):
    return haploid.run(parsed_args=parsed_args,
                       deterministic=DETERMINISTIC,
                       experiment_start_time=experiment_start_time,
                       p_cx=p_cx,
                       p_mut=p_mut,
                       log=log,
                       hof=hof,
                       pop=pop)


def diploid_function(parsed_args, p_cx, p_mut, log, hof, pop, experiment_start_time):
    return diploid.run(parsed_args=parsed_args,
                       deterministic=DETERMINISTIC,
                       experiment_start_time=experiment_start_time,
                       p_cx=p_cx,
                       p_mut=p_mut,
                       log=log,
                       hof=hof,
                       pop=pop)


def get_all_files_in_dir_sorted(dir):
    files = []
    for file_name in os.listdir(dir):
        if file_name.__contains__('ready'):
            files.append(file_name)

    return sorted(files, key=sorter)


def pop_to_dict(pop):
    pop_list = []

    for ind in pop:
        ind_dict = {}
        ind_dict["fitness"] = ind.fitness

    return pop_list


def sorter(item):
    return int(item.split("_")[1])


def store_model(model_class, path):
    f = open(path, "wb")
    pickle.dump(model_class, f)
    f.close()

def remove_file(path):
    os.remove(path)


def create_new_file_name(filename, state, time_as_str, pop_size=None):
    splitted_filename = filename.split("_")
    splitted_filename[0] = state
    splitted_filename[3] = time_as_str

    if pop_size is not None:
        splitted_filename[1] = str(pop_size)

    return "_".join(splitted_filename) + ".json"


def load_model(path):
    if not exists(path):
        return None

    f = open(path, "rb")
    unpickled_model = pickle.load(f)
    f.close()

    return unpickled_model


def get_and_update_experiment_start_time(task_data, now_str):
    if task_data["experiment_start_time"] == "":
        task_data["experiment_start_time"] = now_str
        return now_str
    else:
        return task_data["experiment_start_time"]


def update_parsed_args(parsed_args, task_data):
    for key in task_data["params"]:
        setattr(parsed_args, key, task_data["params"][key])


def rename_file(dir, current_name, new_name):
    os.rename(f"{dir}/{current_name}", f"{dir}/{new_name}")


def create_pickle_file_name(type, experiment_start_time, object_name):
    return f"jobspickles/{type}_{experiment_start_time}_{object_name}.pickle"


def update_pickle_paths_info(pop_path, hof_path, log_path, type, experiment_start_time_str):
    if pop_path == "":
        task_data["history"]["pop_path"] = create_pickle_file_name(type, experiment_start_time_str, "pop")

    if hof_path == "":
        task_data["history"]["hof_path"] = create_pickle_file_name(type, experiment_start_time_str, "hof")

    if log_path == "":
        task_data["history"]["log_path"] = create_pickle_file_name(type, experiment_start_time_str, "log")


def get_pickle_models(pop_path, hof_path, log_path):
    pop = load_model(pop_path)
    hof = load_model(hof_path)
    logs = load_model(log_path)
    return pop, hof, logs


def get_file_state(pop_made, task_data):
    if pop_made >= task_data["max_pop_to_make"]:
        state = "finished"
    else:
        state = "ready"
    return state


def get_pickle_file_paths(task_data):
    pop_path = task_data["history"]["pop_path"]
    hof_path = task_data["history"]["hof_path"]
    log_path = task_data["history"]["log_path"]
    return pop_path, hof_path, log_path


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description='Run this program with "python -u %s" if you want to disable buffering of its output.' % sys.argv[
            0])
    parsed_args = parseArguments(parser=parser)
    print("Argument values:", ", ".join(['%s=%s' % (arg, getattr(parsed_args, arg)) for arg in vars(parsed_args)]))

    jobs_root_dir = "jobs"

    start = time.time()

    while ((time.time() - start) / 3600) < 23:
        print(f"Job is running: {((time.time() - start) / 3600)}h")
        files = get_all_files_in_dir_sorted(jobs_root_dir)

        if len(files) == 0:
            print(f"Stopping job. No tasks available")
            break

        now = datetime.now()
        now_formatted_str = str(now.strftime("%d-%m-%Y-%H-%M-%S.%f"))

        file_to_work_with = files[0]
        locked_file_name = create_new_file_name(filename=file_to_work_with,
                                                state="locked",
                                                time_as_str=now_formatted_str)

        rename_file(jobs_root_dir, file_to_work_with, locked_file_name)

        with open(f"{jobs_root_dir}/{locked_file_name}") as f_json:
            task_data = json.load(f_json)

        update_parsed_args(parsed_args, task_data)

        # TU START
        type_name = task_data["name"]

        pop_path, hof_path, log_path = get_pickle_file_paths(task_data)
        pop, hof, logs = get_pickle_models(pop_path, hof_path, log_path)
        experiment_start_time = get_and_update_experiment_start_time(task_data=task_data,
                                             now_str=now_formatted_str)

        update_pickle_paths_info(pop_path=pop_path,
                                 hof_path=hof_path,
                                 log_path=log_path,
                                 type=type_name,
                                 experiment_start_time_str=experiment_start_time)

        if type_name == "Haploid":
            logs, hof, pop = haploid_function(parsed_args=parsed_args,
                                              p_cx=parsed_args.pxov,
                                              p_mut=parsed_args.pmut,
                                              log=logs,
                                              hof=hof,
                                              pop=pop,
                                              experiment_start_time=experiment_start_time)

        if type_name == "Diploid":
            logs, hof, pop = diploid_function(parsed_args=parsed_args,
                                              p_cx=parsed_args.pxov,
                                              p_mut=parsed_args.pmut,
                                              log=logs,
                                              hof=hof,
                                              pop=pop,
                                              experiment_start_time=experiment_start_time)
        # TU END

        store_model(pop, task_data["history"]["pop_path"])
        store_model(hof, task_data["history"]["hof_path"])
        store_model(logs, task_data["history"]["log_path"])

        pop_made = logs[-1]["trained_pop"]
        task_data["pop_made"] = pop_made

        new_file_state = get_file_state(pop_made=pop_made, task_data=task_data)
        if new_file_state == "finished":
            remove_file(task_data["history"]["pop_path"])
            remove_file(task_data["history"]["hof_path"])
            remove_file(task_data["history"]["log_path"])

        with open(f"{jobs_root_dir}/{locked_file_name}", 'w') as fout:
            json.dump(task_data, fout)

        new_unlocked_file_name = create_new_file_name(filename=locked_file_name,
                                                      state=new_file_state,
                                                      time_as_str=now_formatted_str,
                                                      pop_size=task_data["pop_made"])

        rename_file(jobs_root_dir, locked_file_name, new_unlocked_file_name)
