#!/usr/bin/env python

"""
Script written to run gubbins on output from snippy-clean_full_aln
"""

##Load libraries
import pandas as pd
import glob
import argparse
import sys
import os
import subprocess
from os import listdir
from re import sub

##script in function so that it can be used as a module in the main run_snippy.py
def man(args):

	##Path variables used in script
	outpath = args['out_dir']

	subprocess.run(
		f"bash -c 'source activate working; run_gubbins.py -p gubbins {outpath}clean.full.aln"
			)


##If the script is run directly it will use argparse as input for script, as opposed to input from run_snippy.py
if __name__=='__main__':
	parser = argparse.ArgumentParser(description='Run gubbins on output from snippy, to remove recominative sites. Ensure name of file is clean.core.aln')
	parser.add_argument('--out_dir', '-od', dest='out_dir', help='Directory where snippy out is placed', required=True)

	args = parser.parse_args()


	##Convert the argparse.Namespace to a dictionary: vars(args)
	main(vars(args))
	sys.exit(0)
