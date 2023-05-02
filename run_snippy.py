#!/usr/bin/env python

##Import libraries
import pandas as pd
import subprocess
import glob
import re
import os
import argparse
import make_snippy_tab as snp_tab

##Create arguments to be used in script
parser = argparse.ArgumentParser(
	description="""Pipeline to take your raw fastq files
	(all in one directory), and run them through Snippy
	producing a distance matrix and ML pylogeny"""
	)
parser.add_argument(
	'--input_dir', '-id',
	dest='input_dir',
	help='Directory with input fastq files',
	required=True
	)
parser.add_argument(
	'--output_dir', '-od',
	dest='output_dir',
	help='Directory for output files',
	required=True
        )
parser.add_argument(
	'--snippy_dir', '-sd',
	dest='snippy_dir',
	help='Bin directory with snippy executables, if snippy is not in PATH',
	required=True
	)
parser.add_argument(
	'--ref_dir', '-rd',
	dest='ref_dir',
	help='Bin directory with reference genome for isolates to align to',
	required=True
	)
parser.add_arument(
	'--cpus', '-c',
	dest='cpus',
	help='Number of cpus to use',
	required=True
	)
args = parser.parse_args()

##Set variables and paths


##Produce snippy multi file using make_snipy_tab.py script
snp_tab_dic = {'input_dir':f'{args.input_dir}','out_dir':f'{args.output_dir}'}
snp_tab.main(snp_tab_dic)

##run snippy on snippy multi output (which is just snippy on each individual isolate)
if args.snippy_dir:
	os.chdir(args.snippy_dir)
	subprocess.run(f"bash -c 'source activate working; snippy-multi {args.out_dir}snippy_tab.txt --ref args.ref_dir} --cpus {args.cpus} > {args.out_dir}runme.sh'"
else:

subprocess.run(f"bash -c 'source activate working; {args.out_dir}runme.sh'")
##run snippy clean-core
