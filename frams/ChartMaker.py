import json
from os import listdir
from os.path import isfile, join

import matplotlib.pyplot as plt
import numpy as np


def load_json(file):
    data = json.load(file)
    return data


def convert_path_to_json(prefix, paths):
    jsons = []
    for path in paths:
        f = open(f'{prefix}/{path}')
        jsons.append(json.load(f))
    return jsons


def get_list_of_attributs(attr_name, list, add_as_first=None):
    attributes = []

    if add_as_first is not None:
        attributes.append(add_as_first)

    for el in list:
        attributes.append(el[attr_name])
    return np.array(attributes)


def single_population_chart(all_data,
                            show_avg=False,
                            show_std_dev=False,
                            show_max=False,
                            show_max_hof=False,
                            # available: time, trained_pop
                            x_attribute='trained_pop'):
    data = all_data["logs"]
    fig, ax = plt.subplots()
    x = get_list_of_attributs(x_attribute, data, 0)

    if show_avg:
        y_avg = get_list_of_attributs('avg', data, 0)

        if show_std_dev:
            y_err = get_list_of_attributs('stddev', data, 0)
            ax.fill_between(x, y_avg - y_err, y_avg + y_err, alpha=0.2)

        ax.plot(x, y_avg, color='tab:brown')

    if show_max:
        y_max = get_list_of_attributs('max', data, 0)
        ax.plot(x, y_max, color='tab:red')

    if show_max_hof:
        y_hof = get_list_of_attributs('hof_fitness', data, 0)
        ax.plot(x, y_hof, color='tab:green')

    ax.set_title(all_data["metadata"]["type"])
    ax.set_xlabel(x_attribute)
    ax.set_ylabel("fitness")
    ax.set_ylim(ymin=0)
    ax.set_xlim(xmin=0)


def dual_chart(all_data_1,
               all_data_2,
               # available: time, trained_pop
               x_attribute='trained_pop'):
    data1 = all_data_1["logs"]
    data2 = all_data_2["logs"]

    fig, ax = plt.subplots()
    x_1 = get_list_of_attributs(x_attribute, data1, 0)
    x_2 = get_list_of_attributs(x_attribute, data2, 0)

    y_max_1 = get_list_of_attributs('hof_fitness', data1, 0)
    y_max_2 = get_list_of_attributs('hof_fitness', data2, 0)

    ax.plot(x_1, y_max_1, color='tab:red', label=all_data_1["metadata"]["type"])
    ax.plot(x_2, y_max_2, color='tab:green', label=all_data_2["metadata"]["type"])

    ax.set_ylim(ymin=0)
    ax.set_xlim(xmin=0)
    ax.set_ylabel("fitness")
    ax.set_xlabel(x_attribute)
    ax.legend()

# todo: dodać z metadata infomracje

file_1 = "train_25-05-2022-16-59-22_Diploid.json"
file_2 = "train_25-05-2022-16-59-22_Haploid.json"

# z std. dev
f = open(f'data/{file_1}')
data = load_json(file=f)
single_population_chart(all_data=data, show_avg=True, show_std_dev=True, show_max=True, show_max_hof=True)

f = open(f'data/{file_2}')
data = load_json(file=f)
single_population_chart(all_data=data, show_avg=True, show_std_dev=True, show_max=True, show_max_hof=True)

f_dual_1 = open(f'data/{file_1}')
dual_data_1 = load_json(file=f_dual_1)

f_dual_2 = open(f'data/{file_2}')
dual_data_2 = load_json(file=f_dual_2)

dual_chart(all_data_1=dual_data_1, all_data_2=dual_data_2)
dual_chart(all_data_1=dual_data_1, all_data_2=dual_data_2, x_attribute='time')

plt.show()
f.close()
