from statistics import mean, stdev

import matplotlib.pyplot as plt
import numpy as np

from frams.charts.ChartUtils import get_all_dirs_in, get_all_files_in_dir, get_data


def convert_to_population_values_map(datas):
    data_map = {}
    for x in datas:
        for generation in x["logs"]:
            if generation["trained_pop"] not in data_map:
                data_map[generation["trained_pop"]] = []

            data_map[generation["trained_pop"]].append(generation["hof_fitness"])
    return data_map


def convert_data_map_to_mean(data_map):
    y_mean = []
    x = []
    y_std_dev = []

    y_mean.append(0)
    x.append(0)
    y_std_dev.append(0)

    for k in sorted(data_map.keys()):
        x.append(k)
        list_of_values = data_map[k]
        y_mean.append(mean(list_of_values))

        if len(list_of_values) > 1:
            y_std_dev.append(stdev(list_of_values))
        else:
            y_std_dev.append(0)

    return x, y_mean, y_std_dev


def single_population_chart(ax, x, y_mean, y_std_dev, color="tab:green"):
    x = np.array(x)
    y_mean = np.array(y_mean)
    y_std_dev = np.array(y_std_dev)

    ax.plot(x, y_mean, color=color)
    ax.fill_between(x, y_mean - y_std_dev, y_mean + y_std_dev, alpha=0.2, color=color)

    ax.set_ylim(ymin=0)
    ax.set_xlim(xmin=0)


rootdir = '../data'
for dir in get_all_dirs_in(rootdir):
    haploid_datas = []
    diploid_datas = []
    popsize = None
    p_cx = None
    p_mut = None

    for file in get_all_files_in_dir(dir):
        data = get_data(dir, file)

        popsize = data["metadata"]["population_size"]
        p_cx = data["metadata"]["p_cx"]
        p_mut = data["metadata"]["p_mut"]

        if data["metadata"]["type"] == "Diploid":
            diploid_datas.append(data)

        if data["metadata"]["type"] == "Haploid":
            haploid_datas.append(data)

    haploid_data_map = convert_to_population_values_map(haploid_datas)
    diploid_data_map = convert_to_population_values_map(diploid_datas)

    x_hap, y_mean_hap, y_std_dev_hap = convert_data_map_to_mean(haploid_data_map)
    x_dip, y_mean_dip, y_std_dev_dip = convert_data_map_to_mean(diploid_data_map)

    fig, ax = plt.subplots()
    ax.plot([], [], color='tab:red', label="Diploid")
    ax.plot([], [], color='tab:blue', label="Haploid")
    ax.set_ylabel("Mean fitness (velocity)")
    title = f"Haploid vs diploid. p_cx={p_cx} pmut={p_mut}. Popsize={popsize}"
    ax.set_title(title)

    single_population_chart(ax, x_hap, y_mean_hap, y_std_dev_hap, color='tab:blue')
    single_population_chart(ax, x_dip, y_mean_dip, y_std_dev_dip, color='tab:red')

    plt.savefig(f'{dir}/mean-logs-chart.png')
    plt.show()
