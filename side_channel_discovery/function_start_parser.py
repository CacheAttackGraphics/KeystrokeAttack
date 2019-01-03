__author__ = 'Ajaya Neupane'
import os
from collections import defaultdict,OrderedDict 
import logging
import csv
from encoder import charName

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)


#split at the first occurrence
def keyGenerator(filename):

	return str(filename).split('.',1)[0]

def generateDicts(filename):
	#logger.info("generating list of addresses for keys")
	key_fxn_start = {}

	with open(filename, 'r') as csvfile:
		csv_reader = csv.reader(csvfile, delimiter='\t', quotechar='|')
		for row in csv_reader:
			start_add,fxn_name,lib_name = row[0],row[1], ".".join(row[2].split(".", 2)[:2])
			key_fxn_start[start_add]=(fxn_name, lib_name, int(row[len(row)-1],0))

	return key_fxn_start

def prase_given_pairs():
	path='../results/selectedfeatures.txt'
	pairs = []
	libtypes = []
	csvopen = open(path,'r')
	for row in csvopen:
		values = row.split('_')
		pairs.append(values[0])
		libtypes.append(values[1])
		pairs.append(values[2])
		libtypes.append(values[3])

	return pairs,libtypes

def function_start_parser():

	library_path = '../data/'
	log_folders = os.listdir(library_path)
	logging.debug(log_folders)

	for a_log_folder in log_folders:
		
		#logger.debug('library %s',a_log_folder)
		log_files = os.listdir(library_path+a_log_folder)
			
		all_data = defaultdict(list)

		for a_log_file in log_files:
			#logger.debug('library %s',a_log_file)
			input_file = library_path+a_log_folder+"/"+a_log_file
			if '.func' in a_log_file:
				#logger.debug(a_log_file)
				key_count_dict = generateDicts(input_file)
				all_data[keyGenerator(a_log_file)] = key_count_dict

		logger.debug('number of unique keys %d', len(all_data))
	
	return all_data['0_0']


def find_related_function(pairs,libtypes, function_start_list):

	keys = list(function_start_list.keys())
	set_keys = []
	dict_return = {}
	for a_add in pairs:
		set_keys = [abs(int(int(start_add,0)/0x40) - int(a_add,0)) for start_add in keys]
		dict_return[a_add] = (keys[set_keys.index(min(set_keys))], min(set_keys), function_start_list[keys[set_keys.index(min(set_keys))]])
	return dict_return

def main():
	pairs,libtypes = prase_given_pairs()
	function_start_list = function_start_parser()

	set_key = find_related_function(pairs, libtypes, function_start_list)
	print(set_key)
main()