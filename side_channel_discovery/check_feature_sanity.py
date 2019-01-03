__author__ = 'Ajaya Neupane'
import os
from collections import defaultdict,OrderedDict 
import logging
import csv
from encoder import charName
import itertools
import numpy as np

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

threshold_ins = 5 
#split at the first occurrence

pos_dict = {}

addpair=['0x1f17.libcairo','0xfaf.libcairo']

def keyGenerator(filename):

	return str(filename).split('.',1)[0]


def generateDicts(filename):
	#logger.info("generating list of addresses for keys")
	values = []
	keys = []

	index_list = []
	all_occ = {}

	with open(filename, 'r') as csvfile:
		csv_reader = csv.reader(csvfile, delimiter='\t', quotechar='|')
		for row in csv_reader:
			add_key,value,library_name = row[0],int(row[1]),row[2].split('-')[0]
			key = add_key+"."+library_name.split('.')[0] #4each key belonging to different

			keys.append(key)
			values.append(value)
			
	for no,items in enumerate(addpair):
		try:
			all_occ[no] = [index for index, value in enumerate(keys) if value == items]
			group_length = sum(values[0:max(all_occ[no])]) - sum(values[0:min(all_occ[no])]) 
			print("length",no,all_occ[no],group_length)
		except:
			print("key not found in file",items,filename)
	
	group_distance = sum(values[0:min(all_occ[1])]) - sum(values[0:min(all_occ[0])]) 

	print("pair",group_distance)

def check_sanity(library_path):

	log_folders = os.listdir(library_path)
	logging.debug(log_folders)

	for a_log_folder in log_folders:
		
		logger.debug('library %s',a_log_folder)
		log_files = os.listdir(library_path+a_log_folder)
			
		for a_log_file in log_files:
			#logger.debug('library %s',a_log_file)
			input_file = library_path+a_log_folder+"/"+a_log_file
			statinfo = os.stat(input_file)

			if 'lifespan' not in a_log_file and 'blank' not in a_log_file and '.trimmed' in a_log_file and statinfo.st_size !=0:
				logger.debug(a_log_file)
				generateDicts(input_file)


def main():
	library_path = '../data/'
	check_sanity(library_path)
	#count_addresses()
	#find_add_unique_to_digits()

main()
#distance_between_adds_in_different_pages()