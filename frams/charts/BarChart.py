import matplotlib.pyplot as plt

from ChartUtils import get_all_dirs_in, get_all_files_in_dir, get_data

rootdir = '../data'

set_of_all = []

for dir in get_all_dirs_in(rootdir):
    haploid_velocity = []
    diploid_velocity = []

    p_cx = None
    p_mut = None
    popsize = None
    fitness_type = ""

    for file in get_all_files_in_dir(dir):
        try:
            data = get_data(dir, file)
        except:
            print("EXCEPTION")

        p_cx = data["metadata"]["p_cx"]
        p_mut = data["metadata"]["p_mut"]
        popsize = data["metadata"]["population_size"]
        type_of_data = data["metadata"]["type"]

        if "velocity" in data["metadata"]["hof"][0]:
            fitness_type = "Velocity"
            v = data["metadata"]["hof"][0]["velocity"]
        elif "vertpos" in data["metadata"]["hof"][0]:
            fitness_type = "Vertpos"
            v = data["metadata"]["hof"][0]["vertpos"]
        # v = data["metadata"]["hof"][0]["vertpos"]

        if type_of_data == "Haploid":
            haploid_velocity.append(v)
        else:
            diploid_velocity.append(v)

    set_of_all.append({
        "name": f"[H] Pop={popsize}",
        "data": haploid_velocity
    })

    set_of_all.append({
        "name": f"[D] Pop={popsize}",
        "data": diploid_velocity
    })

    fig1, ax = plt.subplots()
    title = f"Comparison of Haploid and Diploid genotypes in {fitness_type} fitness function."
    ax.set_title(title)
    ax.boxplot([haploid_velocity, diploid_velocity], notch=True)
    ax.set_ylabel(f"Fitness ({fitness_type})")
    plt.xticks([1, 2], ['Haploid', 'Diploid'])
    plt.xlabel(f"Number of fitness function executions. \n Diploid population size is 50. \n Haploid population size is 100.")
    plt.savefig(f'{dir}/boxplot-chart.png')
    # plt.show()

datas = []
names = []
porz = []
tmp = 1

for value in set_of_all:
    if not value["data"]:
        continue

    porz.append(tmp)
    tmp += 1

    datas.append(value["data"])
    names.append(value["name"])

fig2, ax2 = plt.subplots()
title = f"Summary Haploid vs diploid."
ax2.set_title(title)
ax2.boxplot(datas, notch=True)
ax2.set_ylabel("Fitness (velocity)")
plt.xticks(rotation=20)
plt.xticks(porz, names)
plt.savefig(f'{rootdir}/all-barchart.png')
plt.show()