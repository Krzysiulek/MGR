#!/bin/sh

# usuwanie tego co jest tutaj

# pobieranie wszystkiego co jest na polluksie
scp -r inf136224@polluks.cs.put.poznan.pl:/home/inf136224/MGR/frams/data/ /Users/krzysztofczarnecki/Documents/studia/MGR/frams/

# zbiorcze foldery
mkdir /Users/krzysztofczarnecki/Documents/studia/MGR/frams/data/velocity_pcx_0.2_pmut_0.9_hapl_100_dipl_50
mkdir /Users/krzysztofczarnecki/Documents/studia/MGR/frams/data/vertpos_pcx_0.2_pmut_0.9_hapl_100_dipl_50
mkdir /Users/krzysztofczarnecki/Documents/studia/MGR/frams/data/velocity_pcx_0_pmut_0.9_hapl_100_dipl_50
mkdir /Users/krzysztofczarnecki/Documents/studia/MGR/frams/data/vertpos_pcx_0_pmut_0.9_hapl_100_dipl_50

# kopiowanie do zbiorczych folderów
# velocity pcx 0.2
cp /Users/krzysztofczarnecki/Documents/studia/MGR/frams/data/velocity_pcx_0.2_pmut_0.9_popsize_100/*Haploid* /Users/krzysztofczarnecki/Documents/studia/MGR/frams/data/velocity_pcx_0.2_pmut_0.9_hapl_100_dipl_50/
cp /Users/krzysztofczarnecki/Documents/studia/MGR/frams/data/velocity_pcx_0.2_pmut_0.9_popsize_50/*Diploid* /Users/krzysztofczarnecki/Documents/studia/MGR/frams/data/velocity_pcx_0.2_pmut_0.9_hapl_100_dipl_50/

# velocity pcx 0
cp /Users/krzysztofczarnecki/Documents/studia/MGR/frams/data/velocity_pcx_0_pmut_0.9_popsize_100/*Haploid* /Users/krzysztofczarnecki/Documents/studia/MGR/frams/data/velocity_pcx_0_pmut_0.9_hapl_100_dipl_50/
cp /Users/krzysztofczarnecki/Documents/studia/MGR/frams/data/velocity_pcx_0_pmut_0.9_popsize_50/*Diploid* /Users/krzysztofczarnecki/Documents/studia/MGR/frams/data/velocity_pcx_0_pmut_0.9_hapl_100_dipl_50/

# vertpos pcx 0.2
cp /Users/krzysztofczarnecki/Documents/studia/MGR/frams/data/vertpos_pcx_0.2_pmut_0.9_popsize_100/*Haploid* /Users/krzysztofczarnecki/Documents/studia/MGR/frams/data/vertpos_pcx_0.2_pmut_0.9_hapl_100_dipl_50/
cp /Users/krzysztofczarnecki/Documents/studia/MGR/frams/data/vertpos_pcx_0.2_pmut_0.9_popsize_50/*Diploid* /Users/krzysztofczarnecki/Documents/studia/MGR/frams/data/vertpos_pcx_0.2_pmut_0.9_hapl_100_dipl_50/

# vertpos pcx 0
cp /Users/krzysztofczarnecki/Documents/studia/MGR/frams/data/vertpos_pcx_0_pmut_0.9_popsize_100/*Haploid* /Users/krzysztofczarnecki/Documents/studia/MGR/frams/data/vertpos_pcx_0_pmut_0.9_hapl_100_dipl_50/
cp /Users/krzysztofczarnecki/Documents/studia/MGR/frams/data/vertpos_pcx_0_pmut_0.9_popsize_50/*Diploid* /Users/krzysztofczarnecki/Documents/studia/MGR/frams/data/vertpos_pcx_0_pmut_0.9_hapl_100_dipl_50/

# usuwanie niepotrzebych folderów

#find /Users/krzysztofczarnecki/Documents/studia/MGR/frams/data ! -name "*hapl*dipl*" -exec rm -r {} \;
#find /Users/krzysztofczarnecki/Documents/studia/MGR/frams/data/ -type f ! -name "*hapl*dipl*" -exec rm {} \;
#find . ! -name "*.txt" -exec rm -r {} \;