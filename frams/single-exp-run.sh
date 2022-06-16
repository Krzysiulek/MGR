export PYTHONUNBUFFERED=1
export DIR_WITH_FRAMS_LIBRARY=/home/inf136224/MGR/Framsticks50rc20

python3 FramsticksEvolutionSlurmRunner.py -path /home/inf136224/MGR/Framsticks50rc20 -sim "eval-allcriteria.sim;deterministic.sim;sample-period-2.sim" -opt velocity -max_numparts 30 -max_numgenochars 50 -initialgenotype "X(X[N],X[N])" -popsize 100 -generations 50 -hof_size 1