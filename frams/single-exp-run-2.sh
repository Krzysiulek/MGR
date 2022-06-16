#!/bin/sh

# srun -p idss-student --time 24:00:00 -N3 --exclude lab-al-7 -o logs.log -e err-logs.log ~/MGR/frams/single-exp-run.sh &
echo "Starting to execute"

export PYTHONUNBUFFERED=1
export DIR_WITH_FRAMS_LIBRARY=/home/inf136224/MGR/Framsticks50rc20

echo "Running application"
cd /home/inf136224/MGR/frams
python3 FramsticksEvolutionSlurmThreadsRunner.py -path /home/inf136224/MGR/Framsticks50rc20 -sim "eval-allcriteria.sim;deterministic.sim;sample-period-longest.sim" -opt velocity -max_numparts 30 -max_numgenochars 50 -initialgenotype "X(X[N],X[N])" -popsize 50 -generations 50 -hof_size 1
echo "Application executed"