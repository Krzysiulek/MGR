#!/bin/bash

mkdir -p jobs

for i in {1..40}
do
  cp jobstocopy/locked_0_velocity-diploid-cx_do_kopiowania.json jobs/ready_"${i}"_velocity-diploid-cx_0.json
  cp jobstocopy/locked_0_velocity-diploid-nocx_do_kopiowania.json jobs/ready_"${i}"_velocity-diploid-nocx_0.json
  cp jobstocopy/locked_0_velocity-haploid-cx_do_kopiowania.json jobs/ready_"${i}"_velocity-haploid-cx_0.json
  cp jobstocopy/locked_0_velocity-haploid-nocx_do_kopiowania.json jobs/ready_"${i}"_velocity-haploid-nocx_0.json
  cp jobstocopy/locked_0_vertpos-diploid-cx_do_kopiowania.json jobs/ready_"${i}"_vertpos-diploid-cx_0.json
  cp jobstocopy/locked_0_vertpos-diploid-nocx_do_kopiowania.json jobs/ready_"${i}"_vertpos-diploid-nocx_0.json
  cp jobstocopy/locked_0_vertpos-haploid-cx_do_kopiowania.json jobs/ready_"${i}"_vertpos-haploid-cx_0.json
  cp jobstocopy/locked_0_vertpos-haploid-nocx_do_kopiowania.json jobs/ready_"${i}"_vertpos-haploid-nocx_0.json
done

