#!/bin/sh
echo "Starting to execute"

export PYTHONUNBUFFERED=1
export DIR_WITH_FRAMS_LIBRARY=/home/inf136224/MGR/Framsticks50rc20

echo "Running application"
cd /home/inf136224/MGR/frams
python3 FramsticksEvolutionSlurmThreadsRunner2.py
echo "Application executed"
