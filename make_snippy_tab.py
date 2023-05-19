#!/usr/bin/env python

"""
Script to make the input tab delimited file used for snippy_multi. When prompted, input
the path to the directory holding all the fastq files you will be including in the
aligment
"""

##Load libraries
import pandas as pd
import glob
import argparse
import sys
import os
from os import listdir
from re import sub
#from os.path import isfile, join

##Make whole script into function so that the script can be imported by another script
def main(args):

	##Make variables and lists used in script
	mypath = args['input_dir']
	outpath = args['out_dir']

	path_lst_R1 = []
	path_lst_R2 = []
	#file_lst = [s for s in listdir(mypath) if s.endswith('.gz')]
	isolate_name = []
	file_lst_2 = []

	##Add path for each file in a list
	for file in glob.glob(mypath + '*R1*gz'):
		r2_file = sub('_R1', '_R2', file)
		if os.path.isfile(r2_file):
			path_lst_R1.append(file)
			path_lst_R2.append(r2_file)
			file_lst_2.append(sub(mypath, '', file))
		else:
			pass

	path_lst_R1 = sorted(set(path_lst_R1))
	path_lst_R2 = sorted(set(path_lst_R2))

	###Creat a dataframe and insert each isolate to first column
	##creat isolate list, the isolate ID that will be on the first column of your dataframe
	for name in file_lst_2:
		new_name = sub(r'_R.*', '', name)
		isolate_name.append(new_name)
	isolate_name = sorted(set(isolate_name))

	##convert lists to dataframes
	isolate_df = isolate_df = pd.DataFrame(list(zip(isolate_name,path_lst_R1,path_lst_R2)))

	##Write dataframe
	isolate_df.to_csv(outpath + 'snippy_tab.txt', sep="\t",index=False, header=False)

if __name__=='__main__':
	parser = argparse.ArgumentParser()
	parser.add_argument('--input_dir', '-id', dest='input_dir', help='Directory with input reads', required=True)
	parser.add_argument('--out_dir', '-od', dest='out_dir', help='Directory where snippy_tab.txt file will be output', required=True)

	args = parser.parse_args()


	##Convert the argparse.Namespace to a dictionary: vars(args)
	main(vars(args))
	sys.exit(0)


'''
Unused...for now
'''
##Loop through path list with isoalte name and append file paths to 1st(R1) and 2nd(R2) column of isolate dataframe
#for isolate in isolates_df:
#	result1 = [v for v in path_lst if str(isolate)+'_R1' in v]
#	result2 = [v for v in path_lst if str(isolate)+'_R2' in v]

