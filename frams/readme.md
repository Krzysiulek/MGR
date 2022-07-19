# Żeby odpalić FramsicksEvolution.py

Parametry:
```bash
-path C:\Users\Lenovo\OneDrive\Pulpit\MGR\Framsticks50rc20 -sim eval-allcriteria.sim;deterministic.sim;sample-period-2.sim; -opt vertpos -max_numparts 30 -max_numgenochars 50 -initialgenotype /*9*/BLU -popsize 100 -generations 20 -hof_size 1 -hof_savefile HoF-f9-%%M-%%N.gen
```

Environment Variables:
```bash
PYTHONUNBUFFERED=1;DIR_WITH_FRAMS_LIBRARY=C:\Users\Lenovo\OneDrive\Pulpit\MGR\Framsticks50rc20
```

# Pomysły na pracę:
- testy dla małych pop-size
- testy dla dużych pop-size
- testy na zbiezność
- Przystosowanie pod szybkość
- Wyjaśnienie co to jest Framstik
- Dla każdego eksperymentu, odpalić framsticka i wkleić jego zdjęcie


# Uruchamianie:
## Opis skryptów:

## Pomoce przy uruchomieniu:
#### Podglądanie aktualnych jobów:
```shell
watch -n 5 "squeue -u inf136224 -t PD | wc -l \\
&& squeue -u inf136224 -t R | wc -l \\
&& squeue --format=\"%.18i %.9P %.30j %.8u %.8T %.10M %.9l %.6D %R\" -u inf136224 -t R \\
&& squeue -u inf136224 -t PD --start | grep Resources"


squeue --format="%.18i %.9P %.30j %.8u %.8T %.10M %.9l %.6D %R" -u inf136224 -t R
```

### Uruchamianie SLURM:
```shell
sbatch -p idss-student --time 24:00:00 -N1 --exclude lab-al-7 -o logs.log -e err.log  ~/MGR/frams/run-vertpos-diploid-50.sh
sbatch -p idss-student --time 24:00:00 -N1 --exclude lab-al-7 -o logs.log -e err.log  ~/MGR/frams/run-vertpos-haploid-100.sh

sbatch -p idss-student --time 24:00:00 -N1 --exclude lab-al-7 -o logs.log -e err.log  ~/MGR/frams/run-velocity-diploid-50.sh
sbatch -p idss-student --time 24:00:00 -N1 --exclude lab-al-7 -o logs.log -e err.log  ~/MGR/frams/run-velocity-haploid-100.sh
```

```shell
sbatch -p idss-student --time 24:00:00 -N1 --exclude lab-al-7 -o queuelogs.log -e queueerr.log  ~/MGR/frams/run-queue.sh
```


#### Velocity 50
```shell
sbatch -p idss-student --time 24:00:00 -N1 --exclude lab-al-7 -o logs50.log -e err-logs50.log  ~/MGR/frams/run-velocity-50.sh
```

#### Velocity 100
```shell
sbatch -p idss-student --time 24:00:00 -N1 --exclude lab-al-7 -o logs100.log -e err-logs100.log  ~/MGR/frams/run-velocity-100.sh
```

#### Vertpos 50
```shell
srun -p idss-student --time 24:00:00 -N1 --exclude lab-al-7 -o logs50.log -e err-logs50.log  ~/MGR/frams/run-vertpos-50.sh &
```

#### Vertpos 100
```shell
srun -p idss-student --time 24:00:00 -N10 --exclude lab-al-7 -o logs100.log -e err-logs100.log  ~/MGR/frams/run-vertpos-100.sh &
```

```shell
#!/bin/sh

for i in {0..2..1}
do
  echo "Running $i"
  sbatch -p idss-student --time 24:00:00 -N1 --exclude lab-al-7 -o logs100.log -e err-logs100.log  ~/MGR/frams/run-vertpos-100.sh 
  sbatch -p idss-student --time 24:00:00 -N1 --exclude lab-al-7 -o logs50.log -e err-logs50.log  ~/MGR/frams/run-vertpos-50.sh
done
```

# Notatki
## 07.06.2022
- slurm
- jedno kryterium
  - vertpos lub velocity -> period2
- vertpos -> period2
- velocity -> period-longest