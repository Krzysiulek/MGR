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


def single_population_chart(data,
                            show_avg=False,
                            show_std_dev=False,
                            show_max=False,
                            show_max_hof=False):
    fig, ax = plt.subplots()
    x = get_list_of_attributs('trained_pop', data, 0)

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

    ax.set_ylim(ymin=0)
    ax.set_xlim(xmin=0)


# z std. dev
f = open('data/train_08-05-2022-20-18-47.json')
data = load_json(file=f)["logs"]
# single_population_chart(data, show_max=True, show_max_hof=True)
# single_population_chart(data, show_avg=True, show_std_dev=True)
single_population_chart(data, show_avg=True, show_std_dev=True, show_max=True, show_max_hof=True)

# dużo z maxem
mypath = 'data'
onlyfiles = [f for f in listdir(mypath) if isfile(join(mypath, f))]
# make_charts_with_max(convert_path_to_json('data', onlyfiles))

# wszystkie
# datas = convert_path_to_json('data', onlyfiles)
# for da in datas:
#     make_chart_with_std_dev(da)


plt.show()
f.close()
