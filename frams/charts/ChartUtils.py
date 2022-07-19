import os

from ChartMaker import load_json


def should_skip_folder(dir_name):
    to_skip = [".gitkeep", "history"]
    return to_skip.__contains__(dir_name)


def should_skip_file(filename):
    to_skip = ["fig.png", "boxplot-chart.png", "all-logs-chart.png", "mean-logs-chart.png"]
    return to_skip.__contains__(filename)


def get_all_dirs_in(rootdir):
    dirs = []

    for dir_name in os.listdir(rootdir):
        d = os.path.join(rootdir, dir_name)

        if should_skip_folder(dir_name):
            continue

        if os.path.isdir(d):
            dirs.append(d)

    dirs.sort()
    return dirs


def get_all_files_in_dir(dir):
    files = []
    for file_name in os.listdir(dir):
        if should_skip_file(file_name):
            continue
        files.append(file_name)

    return files


def get_data(dir, filename):
    f = open(f"{dir}/{filename}")
    data = load_json(file=f)

    return data
