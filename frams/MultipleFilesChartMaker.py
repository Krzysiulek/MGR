import json
from os import listdir
from os.path import isfile, join

import matplotlib.pyplot as plt
import numpy as np
import math

def roundup(x, roundup=100):
    return int(math.ceil(x / roundup)) * roundup

import os
plt.rcParams.update({'figure.max_open_warning': 0})
plt.rcParams["figure.autolayout"] = True

from ChartMaker import load_json, get_list_of_attributs

def get_max_of_files(data):
    max_x = data["logs"][-1]["trained_pop"]
    max_y = data["metadata"]["hof"][0]["velocity"]
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


rootdir = 'data'
for dir_name in os.listdir(rootdir):
    d = os.path.join(rootdir, dir_name)

    if dir_name == ".gitkeep" or dir_name == "history":
        continue


    if os.path.isdir(d):
        fig, ax = plt.subplots()

        ax.plot([], [], color='tab:red', label="Diploid")
        ax.plot([], [], color='tab:blue', label="Haploid")

        max_x = 0
        max_y = 0

        for log_file_name in os.listdir(d):
            if log_file_name == "fig.png":
                continue

            print(f"Creating {d}/{log_file_name}")
            f = open(f"{d}/{log_file_name}")
            data = load_json(file=f)
            single_population_chart(fig, ax, data, show_max_hof=True)

            x, y = get_max_of_files(data)
            if x > max_x:
                max_x = x
            if y > max_y:
                max_y = y

        plt.xticks(np.arange(0, roundup(max_x), roundup(max_x / 10, 1000)))
        plt.yticks(np.arange(0, max_y * 1.1, max_y / 10))

    plt.savefig(f'{d}/fig.png')
    plt.show()
