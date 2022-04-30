rem To learn about all available options of the .py algorithm below, add "-h" to its parameters.
rem Use the source code of the examples as a starting point for your customizations.
rem Example usage:

set DIR_WITH_FRAMS_LIBRARY=C:\Users\Lenovo\OneDrive\Pulpit\Framsticks50rc20\Framsticks50rc20


for %%M in (0,005,010,020,030,040,050) do (
	for /L %%N in (1,1,10) do (
		python FramsticksEvolution.py ^
		-path %DIR_WITH_FRAMS_LIBRARY% ^
		-sim eval-allcriteria.sim;deterministic.sim;sample-period-2.sim;f9-mut-%%M.sim  ^
		-opt vertpos ^
		-max_numparts 30 ^
		-max_numgenochars 50 ^
		-initialgenotype /*9*/BLU   ^
		-popsize 20    ^
		-generations 80 ^
		-hof_size 1 ^
		-hof_savefile HoF-f9-%%M-%%N.gen
		))