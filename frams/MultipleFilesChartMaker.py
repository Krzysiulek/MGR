import json
from os import listdir
from os.path import isfile, join

import matplotlib.pyplot as plt
import numpy as np

import os
plt.rcParams.update({'figure.max_open_warning': 0})
plt.rcParams["figure.autolayout"] = True

from ChartMaker import load_json, get_list_of_attributs

def get_max_of_files(data):
    max_x = data["logs"][-1]["trained_pop"]
    max_y = max(data["metadata"]["hof"][0]["velocity"], data["metadata"]["hof"][0]["distance"])
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

    x = get_list_of_attributs(x_attribute, data, 0)

    if show_max_hof:
        color = "tab:red"
        if type == "Haploid":
            color = "tab:blue"

        y_hof = get_list_of_attributs('hof_fitness', data, 0)
        ax.plot(x, y_hof, color=color)


    title = f"{type} pcx={p_cx} pmut={p_mut}"
    ax.set_title(title)
    ax.set_xlabel(x_attribute)
    ax.set_ylabel("fitness")
    ax.set_ylim(ymin=0)
    ax.legend()
    ax.set_xlim(xmin=0)


rootdir = 'data'
for dir_name in os.listdir(rootdir):
    d = os.path.join(rootdir, dir_name)

    if dir_name == ".gitkeep":
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
                max_x = x + 50
            if y > max_y:
                max_y = y + 50

        plt.xticks(np.arange(0, max_x, max_x / 10))
        plt.yticks(np.arange(0, max_y, max_y / 10))

    plt.savefig(f'{d}/fig.png')
    # plt.show()




results_dict = {}
for p_cross in [1, 0.8, 0.6, 0.4, 0.2, 0.1, 0.05, 0.01]:
    results_dict[p_cross] = {}
    for p_mut in [1, 0.8, 0.6, 0.4, 0.2, 0.1, 0.05, 0.01]:
        results_dict[p_cross][p_mut] = {"haploid": {"max_fitness": 0, "max_pop": 0},
                                        "diploid": {"max_fitness": 0, "max_pop": 0}}

rootdir = 'data'
for dir_name in os.listdir(rootdir):
    d = os.path.join(rootdir, dir_name)

    if dir_name == ".gitkeep":
        continue

    if os.path.isdir(d):
        max_population_haploid = 0
        max_fitness_haploid = 0

        max_population_diploid = 0
        max_fitness_diploid = 0

        p_cx = 0
        p_mut = 0


        for log_file_name in os.listdir(d):
            if log_file_name == "fig.png":
                continue

            print(f"Tableka {d}/{log_file_name}")
            f = open(f"{d}/{log_file_name}")
            data = load_json(file=f)

            p_cx = data["metadata"]["p_cx"]
            p_mut = data["metadata"]["p_mut"]

            x, y = get_max_of_files(data)
            if data["metadata"]["type"] == "Haploid":
                if x > max_population_haploid:
                    max_population_haploid = x
                if y > max_fitness_haploid:
                    max_fitness_haploid = y
            else:
                if x > max_population_diploid:
                    max_population_diploid = x
                if y > max_fitness_diploid:
                    max_fitness_diploid = y

        results_dict[p_cx][p_mut]["haploid"]["max_fitness"] = max_fitness_haploid
        results_dict[p_cx][p_mut]["diploid"]["max_fitness"] = max_fitness_diploid

        results_dict[p_cx][p_mut]["haploid"]["max_pop"] = max_population_haploid
        results_dict[p_cx][p_mut]["diploid"]["max_pop"] = max_population_diploid


def get_attr(p_mut, p_cx, type, key):
    import math
    return math.floor(results_dict[p_cx][p_mut][type][key])


co_printowac = "max_fitness"
type = "haploid"

def print_table(co_printowac, type):
    print()
    print()
    print(f"Pokazuje dla {co_printowac}, {type}")
    print("{:<10} {:<10} {:<10} {:<10} {:<10} {:<10} {:<10} {:<10} {:<10}".format("pm\pc", "1", "0.8", "0.6", "0.4",
                                                                                  "0.2", "0.1", "0.05", "0.01"))
    for p_mut in [1, 0.8, 0.6, 0.4, 0.2, 0.1, 0.05, 0.01]:
        print(
            "{:<10} {:<10} {:<10} {:<10} {:<10} {:<10} {:<10} {:<10} {:<10}".
                format(p_mut,
                       get_attr(p_mut, 1, type, co_printowac),
                       get_attr(p_mut, 0.8, type, co_printowac),
                       get_attr(p_mut, 0.6, type, co_printowac),
                       get_attr(p_mut, 0.4, type, co_printowac),
                       get_attr(p_mut, 0.2, type, co_printowac),
                       get_attr(p_mut, 0.1, type, co_printowac),
                       get_attr(p_mut, 0.05, type, co_printowac),
                       get_attr(p_mut, 0.01, type, co_printowac)))

print_table("max_fitness", "haploid")