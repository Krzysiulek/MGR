import math
import os

import matplotlib.pyplot as plt
import numpy as np

from ChartMaker import load_json, get_list_of_attributs
from ChartUtils import get_all_dirs_in, should_skip_file


def roundup(x, roundup=100):
    return int(math.ceil(x / roundup)) * roundup


plt.rcParams.update({'figure.max_open_warning': 0})
plt.rcParams["figure.autolayout"] = True


def get_max_of_files(data):
    max_x = data["logs"][-1]["trained_pop"]

    if "velocity" in data["metadata"]["hof"][0]:
        max_y = data["metadata"]["hof"][0]["velocity"]
    elif "vertpos" in data["metadata"]["hof"][0]:
        max_y = data["metadata"]["hof"][0]["vertpos"]

    return max_x, max_y


def single_population_chart(fig,
                            ax,
                            all_data,
                            show_max_hof=False,
                            x_attribute='trained_pop'):
    data = all_data["logs"]
    type = all_data["metadata"]["type"]
    p_cx = all_data["metadata"]["p_cx"]
    p_mut = all_data["metadata"]["p_mut"]
    popsize = all_data["metadata"]["population_size"]

    x = get_list_of_attributs(x_attribute, data, 0)

    if show_max_hof:
        color = "tab:red"
        if type == "Haploid":
            color = "tab:blue"

        y_hof = get_list_of_attributs('hof_fitness', data, 0)
        ax.plot(x, y_hof, color=color)

    title = f"Haploid vs diploid. p_cx={p_cx} pmut={p_mut}. Popsize={popsize}"
    ax.set_title(title)
    ax.set_xlabel(x_attribute)
    ax.set_ylabel("Fitness (velocity)")
    ax.set_ylim(ymin=0)
    ax.legend()
    ax.set_xlim(xmin=0)


# rootdir = 'data/history/slurm_exp1_fail'
rootdir = 'data'
for dir in get_all_dirs_in(rootdir):
    fig, ax = plt.subplots()

    ax.plot([], [], color='tab:red', label="Diploid")
    ax.plot([], [], color='tab:blue', label="Haploid")

    max_x = 0
    max_y = 0

    for log_file_name in os.listdir(dir):
        if should_skip_file(log_file_name):
            continue

        print(f"Creating {dir}/{log_file_name}")
        f = open(f"{dir}/{log_file_name}")

        try:
            data = load_json(file=f)
        except Exception:
            continue

        single_population_chart(fig, ax, data, show_max_hof=True)

        x, y = get_max_of_files(data)
        if x > max_x:
            max_x = x
        if y > max_y:
            max_y = y

    # plt.xticks(np.arange(0, roundup(max_x), roundup(max_x / 10, 1000)))
    # plt.yticks(np.arange(0, max_y * 1.1, max_y / 10))
    plt.xlabel(f"{dir}")

    plt.savefig(f'{dir}/all-logs-chart.png')
    plt.show()
