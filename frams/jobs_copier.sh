#!/bin/bash
for i in {1..50}
do
   cp jobs/locked_0_diploid_do_kopiowania.json jobs/ready_${i}_diploid_0.json
   cp jobs/locked_0_haploid_do_kopiowania.json jobs/ready_${i}_haploid_0.json
done
