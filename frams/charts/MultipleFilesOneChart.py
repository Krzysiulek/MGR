from frams.charts.ChartUtils import get_all_dirs_in, get_all_files_in_dir, get_data

haploid_datas = []
diploid_datas = []

rootdir = 'data'
for dir in get_all_dirs_in(rootdir):
    for file in get_all_files_in_dir(dir):
        data = get_data(dir, file)

        if data["metadata"]["type"] == "Diploid":
            diploid_datas.append(data)

        if data["metadata"]["type"] == "Haploid":
            haploid_datas.append(data)



