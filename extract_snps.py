#!/usr/bin/env python

"""
Script written to extract snps from gubbins output using snippy snp-sites
"""

##Load libraries
import pandas as pd
import argparse
import re
import subprocess


##script in function so that it can be used as a module in the main run_snippy.py
def main(args):

	##Path variables used in script
	outpath = args['out_dir']
	snp_dir = args['snp_dir']
	snp_dir = re.sub('bin/', 'binaries/linux/', snp_dir)

	with open(f'{outpath}clean.core.aln') as snp_sites
		subprocess.run(
			f"bash -c 'source activate working; {snp_dir}snp-sites -c {outpath}gubbins.filtered_polymorphic_sites.fasta",
				stdout=snp_sites)


##If the script is run directly it will use argparse as input for script, as opposed to input from run_snippy.py
if __name__=='__main__':
	parser = argparse.ArgumentParser(description='Run gubbins on output from snippy, to remove recominative sites. Ensure name of file is clean.core.aln')
	parser.add_argument('--out_dir', '-od', dest='out_dir', help='Directory where snippy out is placed', required=True)

	args = parser.parse_args()


	##Convert the argparse.Namespace to a dictionary: vars(args)
	main(vars(args))
	sys.exit(0)
