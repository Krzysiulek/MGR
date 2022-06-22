#!/bin/sh

# srun -p idss-student --time 24:00:00 -N3 --exclude lab-al-7 -o logs.log -e err-logs.log ~/MGR/frams/run-velocity-100.sh &
echo "Starting to execute"

export PYTHONUNBUFFERED=1
export DIR_WITH_FRAMS_LIBRARY=/home/inf136224/MGR/Framsticks50rc20

echo "Running application"
cd /home/inf136224/MGR/frams
python3 FramsticksEvolutionSlurmThreadsRunner.py -path /home/inf136224/MGR/Framsticks50rc20 -sim "eval-allcriteria.sim;deterministic.sim;sample-period-longest.sim" -opt velocity -max_numparts 30 -max_numgenochars 50 -initialgenotype "X(X[N],X[N])" -popsize 100 -generations 50 -hof_size 1
echo "Application executed"

# rm -rf /Users/krzysztofczarnecki/Documents/studia/MGR/frams/data/pcx_0.2_pmut_0.9_popsize_100 && rm -rf /Users/krzysztofczarnecki/Documents/studia/MGR/frams/data/pcx_0.2_pmut_0.9_popsize_50 && scp -r inf136224@polluks.cs.put.poznan.pl:/home/inf136224/MGR/frams/data/pcx_0.2_pmut_0.9_popsize_100 /Users/krzysztofczarnecki/Documents/studia/MGR/frams/data/pcx_0.2_pmut_0.9_popsize_100 && scp -r inf136224@polluks.cs.put.poznan.pl:/home/inf136224/MGR/frams/data/pcx_0.2_pmut_0.9_popsize_50 /Users/krzysztofczarnecki/Documents/studia/MGR/frams/data/pcx_0.2_pmut_0.9_popsize_50
# Riafah3eesho
# watch -n 1 squeue -u inf136224

# cd ~/MGR/frams/ && srun -p idss-student --time 24:00:00 -N2 --exclude lab-al-7 -o logs100.log -e err-logs100.log --test-only  ~/MGR/frams/run-velocity-100.sh &
# cd ~/MGR/frams/ && srun -p idss-student --time 24:00:00 -N1 --exclude lab-al-7 -o logs100.log -e err-logs100.log  ~/MGR/frams/run-velocity-100.sh &
# cd ~/MGR/frams/ && srun -p idss-student --time 24:00:00 -N1 --exclude lab-al-7 -o logs50.log -e err-logs50.log  ~/MGR/frams/run-velocity-50.sh &

# cd ~/MGR/frams/ && sbatch -p idss-student --time 24:00:00 -N1 --exclude lab-al-7 -o logs100.log -e err-logs100.log  ~/MGR/frams/run-velocity-100.sh &
# cd ~/MGR/frams/ && sbatch -p idss-student --time 24:00:00 -N1 --exclude lab-al-7 -o logs50.log -e err-logs50.log  ~/MGR/frams/run-velocity-50.sh &
# cd ~/MGR/frams/ && sbatch -p idss-student --time 24:00:00 -N1 --exclude lab-al-7 -o logs50.log -e err-logs50.log  ~/MGR/frams/run-vertpos-50.sh &
# cd ~/MGR/frams/ && sbatch -p idss-student --time 24:00:00 -N1 --exclude lab-al-7 -o logs50.log -e err-logs50.log  ~/MGR/frams/run-vertpos-100.sh &