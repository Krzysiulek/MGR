echo "Starting to execute"

export PYTHONUNBUFFERED=1
export DIR_WITH_FRAMS_LIBRARY=/home/inf136224/MGR/Framsticks50rc20

echo "Installing required libraries"
pip3 install deap
pip3 install numpy
echo "Installing required libraries ended"

echo "Running application"
python3 FramsticksEvolutionSlurmRunner.py -path /home/inf136224/MGR/Framsticks50rc20 -sim "eval-allcriteria.sim;deterministic.sim;sample-period-longest.sim" -opt velocity -max_numparts 30 -max_numgenochars 50 -initialgenotype "X(X[N],X[N])" -popsize 100 -generations 50 -hof_size 1
echo "Application executed"