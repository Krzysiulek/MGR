import matplotlib.pyplot as plt

from frams.charts.ChartUtils import get_all_dirs_in, get_all_files_in_dir, get_data


def get_fitness_type(data):
    fitness_type = ""

    if "velocity" in data["metadata"]["hof"][0]:
        fitness_type = "Velocity"
    elif "vertpos" in data["metadata"]["hof"][0]:
        fitness_type = "Vertpos"
    return fitness_type


rootdir = '../data'
for dir in get_all_dirs_in(rootdir):
    haploid_lenghts = []
    diploid_lenghts = []
    fitness_type = ""

    for file in get_all_files_in_dir(dir):

        try:
            data = get_data(dir, file)
        except Exception:
            print(f"Exception in [{dir}/{file}]")
            continue

        type = data["metadata"]["type"]
        fitness_type = get_fitness_type(data)

        if type == "Diploid":
            diploid_lenghts.append(len(data["metadata"]["hof"][0]["genotype"][0]))
            diploid_lenghts.append(len(data["metadata"]["hof"][0]["genotype"][1]))
        elif type == "Haploid":
            haploid_lenghts.append(len(data["metadata"]["hof"][0]["genotype"][0]))

    if len(diploid_lenghts) == 0 or len(haploid_lenghts) == 0:
        continue

    fig1, ax = plt.subplots()
    ax.boxplot([haploid_lenghts, diploid_lenghts], notch=True)
    plt.xticks([1, 2], ['Haploid', 'Diploid'])
    ax.set_ylabel(f"Genotype lengths ({fitness_type})")

    title = f"Comparison of Haploid and Diploid genotypes lengths in {fitness_type} fitness function."
    ax.set_title(title)

    plt.show()


# todo wykres fitness vs długość genotypu
