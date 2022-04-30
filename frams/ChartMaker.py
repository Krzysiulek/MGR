import json
import matplotlib.pyplot as plt
import numpy as np
from os import listdir
from os.path import isfile, join

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


def make_charts_with_max(list_of_datas):
    fig, ax = plt.subplots()

    for data in list_of_datas:
        x = get_list_of_attributs('trained_pop', data, 0)
        y = get_list_of_attributs('max', data, 0)

        ax.plot(x, y, color='tab:green')
        # ax.set_ylim(ymin=0)
        # ax.set_xlim(xmin=0)

def make_chart_with_std_dev(data):
    fig, ax = plt.subplots()

    x = get_list_of_attributs('trained_pop', data, 0)
    y = get_list_of_attributs('avg', data, 0)
    y_err = get_list_of_attributs('stddev', data, 0)

    ax.fill_between(x, y - y_err, y + y_err, alpha=0.2)
    ax.plot(x, y, color='tab:brown')
    # ax.set_ylim(ymin=0)
    # ax.set_xlim(xmin=0)

# z std. dev
f = open('data/train_29-03-2022-11-02-20.json')
data = json.load(f)
make_chart_with_std_dev(data)

# dużo z maxem
mypath = 'data'
onlyfiles = [f for f in listdir(mypath) if isfile(join(mypath, f))]
make_charts_with_max(convert_path_to_json('data', onlyfiles))

# wszystkie
datas = convert_path_to_json('data', onlyfiles)
# for da in datas:
#     make_chart_with_std_dev(da)


plt.show()
f.close()