#!/bin/sh

rm -rf /Users/krzysztofczarnecki/Documents/studia/MGR/frams/data/velocity_pcx_0.2_pmut_0.9_popsize_100
rm -rf /Users/krzysztofczarnecki/Documents/studia/MGR/frams/data/velocity_pcx_0.2_pmut_0.9_popsize_50
rm -rf /Users/krzysztofczarnecki/Documents/studia/MGR/frams/data/vertpos_pcx_0.2_pmut_0.9_popsize_100
rm -rf /Users/krzysztofczarnecki/Documents/studia/MGR/frams/data/vertpos_pcx_0.2_pmut_0.9_popsize_50

scp -r inf136224@polluks.cs.put.poznan.pl:/home/inf136224/MGR/frams/data/velocity_pcx_0.2_pmut_0.9_popsize_100 /Users/krzysztofczarnecki/Documents/studia/MGR/frams/data/velocity_pcx_0.2_pmut_0.9_popsize_100
scp -r inf136224@polluks.cs.put.poznan.pl:/home/inf136224/MGR/frams/data/velocity_pcx_0.2_pmut_0.9_popsize_50 /Users/krzysztofczarnecki/Documents/studia/MGR/frams/data/velocity_pcx_0.2_pmut_0.9_popsize_50
scp -r inf136224@polluks.cs.put.poznan.pl:/home/inf136224/MGR/frams/data/vertpos_pcx_0.2_pmut_0.9_popsize_100 /Users/krzysztofczarnecki/Documents/studia/MGR/frams/data/vertpos_pcx_0.2_pmut_0.9_popsize_100
scp -r inf136224@polluks.cs.put.poznan.pl:/home/inf136224/MGR/frams/data/vertpos_pcx_0.2_pmut_0.9_popsize_50 /Users/krzysztofczarnecki/Documents/studia/MGR/frams/data/vertpos_pcx_0.2_pmut_0.9_popsize_50

rm -rf /Users/krzysztofczarnecki/Documents/studia/MGR/frams/data/vertpos_pcx_0.2_pmut_0.9_hapl_100_dipl_50
rm -rf /Users/krzysztofczarnecki/Documents/studia/MGR/frams/data/velocity_pcx_0.2_pmut_0.9_hapl_100_dipl_50

mkdir /Users/krzysztofczarnecki/Documents/studia/MGR/frams/data/velocity_pcx_0.2_pmut_0.9_hapl_100_dipl_50
mkdir /Users/krzysztofczarnecki/Documents/studia/MGR/frams/data/vertpos_pcx_0.2_pmut_0.9_hapl_100_dipl_50

cp /Users/krzysztofczarnecki/Documents/studia/MGR/frams/data/velocity_pcx_0.2_pmut_0.9_popsize_100/*Haploid* /Users/krzysztofczarnecki/Documents/studia/MGR/frams/data/velocity_pcx_0.2_pmut_0.9_hapl_100_dipl_50/
cp /Users/krzysztofczarnecki/Documents/studia/MGR/frams/data/velocity_pcx_0.2_pmut_0.9_popsize_50/*Diploid* /Users/krzysztofczarnecki/Documents/studia/MGR/frams/data/velocity_pcx_0.2_pmut_0.9_hapl_100_dipl_50/

cp /Users/krzysztofczarnecki/Documents/studia/MGR/frams/data/vertpos_pcx_0.2_pmut_0.9_popsize_100/*Haploid* /Users/krzysztofczarnecki/Documents/studia/MGR/frams/data/vertpos_pcx_0.2_pmut_0.9_hapl_100_dipl_50/
cp /Users/krzysztofczarnecki/Documents/studia/MGR/frams/data/vertpos_pcx_0.2_pmut_0.9_popsize_50/*Diploid* /Users/krzysztofczarnecki/Documents/studia/MGR/frams/data/vertpos_pcx_0.2_pmut_0.9_hapl_100_dipl_50/