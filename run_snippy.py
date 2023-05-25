#!/usr/bin/env python

##Import libraries
import pandas as pd
import subprocess
import glob
import re
import os
import argparse
import make_snippy_tab as snp_tab
import run_gubbins as gubbins
import extract_snps as ex_snps

##Create arguments to be used in script
parser = argparse.ArgumentParser(
	description="""Pipeline to take your raw fastq files
	(all in one directory), and run them through Snippy
	producing a distance matrix and ML pylogeny. Ensure paths
	end in a '/' and that all provided paths to directories are
	absolute paths, not relative"""
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
	required=False
	)
parser.add_argument(
	'--ref_dir', '-rd',
	dest='ref_dir',
	help='Path to reference genome (and reference genome) for isolates to align to',
	required=True
	)
parser.add_argument(
	'--cpus', '-c',
	dest='cpus',
	help='Number of cpus to use',
	required=True
	)
args = parser.parse_args()

##Function used to append #!/bin/sh to top on runme.sh so that it can work with subpreocess
def line_prepender(filename, line):
    with open(filename, 'r+') as f:
        content = f.read()
        f.seek(0, 0)
        f.write(line.rstrip('\r\n') + '\n' + content)

##Produce snippy multi file using make_snipy_tab.py script
snp_tab_dic = {'input_dir':f'{args.input_dir}','out_dir':f'{args.output_dir}'}
snp_tab.main(snp_tab_dic)


##Run snippy-multi output (which is just snippy on each individual isolate)
if args.snippy_dir:
	os.chdir(args.snippy_dir)
	with open(f'{args.output_dir}runme.sh', 'w') as run_file:
		subprocess.run(
			[
			'./snippy-multi', f'{args.output_dir}snippy_tab.txt',
			f'--ref {args.ref_dir}',
			f' --cpus {args.cpus}'
			],
			stdout=run_file
				)
else:
	with open(f'{args.output_dir}runme.sh', 'w') as run_file:
		subprocess.run(
			[
			'./snippy-multi', f'{args.output_dir}snippy_tab.txt',
			f'--ref {args.ref_dir}',
			f' --cpus {args.cpus}'
			],
			stdout=run_file
				)
####Alter runme.sh script
##Prepend #!/bin/sh to
os.chdir(args.output_dir)
line_prepender('runme.sh', '#!/bin/sh')

##Add path to snippy bin in 'runme.sh', as it creates complications further on if not
subprocess.run(
	[
	'sed', '-i', f's|snippy |{args.snippy_dir}snippy |', 'runme.sh'
	]
		)

subprocess.run(
	[
	'sed', '-i', f's|snippy-core|{args.snippy_dir}snippy-core|', 'runme.sh'
	]
		 )
##Add output directory to snippy output
subprocess.run(
	[
	'sed', '-i', f's|outdir |outdir {args.output_dir}|', 'runme.sh'
	]
		)
##Run runme.sh (which runs snippy on all isolates in directory and snippy-core)
os.chdir(args.output_dir)
subprocess.run(
	[
	'chmod', '+x', f'./runme.sh'
	]
		)

subprocess.run(
	f'./runme.sh'
		)

##Check to see if all isolates ran properly by checking for output in each folder
for file in glob.glob(f'{args.output_dir}' + '*R1*gz'):

	##create variable that gives same string as directory for each isolate analysed
	isolate_dir = re.sub(r'_R.*', '', file)
	os.chdir(f'{args.output_dir}')

	##check to see if the directory for each
	if os.path.isfile(isolate_dir + '/snps.aligned.fa'):
		pass
	else:
		print(f'Isolate {isolate_dir} did not finish properly, check log file for isolate')

##run snippy clean-core
if args.snippy_dir:
	os.chdir(args.snippy_dir)
	with open (f'{args.output_dir}clean.core.aln', 'w') as clean_core:
		subprocess.run(
			[
			'./snippy-clean_full_aln', f'{args.output_dir}core.full.aln'
			],
			stdout=clean_core
				)
else:
	with open (f'{args.output_dir}clean.core.aln', 'w') as clean_core:
		subprocess.run(
			[
			'./snippy-clean_full_aln', f'{args.output_dir}core.full.aln',
			],
			stdout=clean_core
				)

##Run gubbins by using imported run_gubbins script
gubbins_dic = {'out_dir':f'{args.output_dir}'}
gubbins.main(gubbins_dic)

##extract snps from gubbins output
snp_sites_dic = {'out_dir':f'{args.output_dir}','snp_dir':f'{args.snippy_dir}'}
ex_snps.main(snp_sites_dic)
