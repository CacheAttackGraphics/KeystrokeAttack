import logging

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

import os
from collections import defaultdict
import csv
import numpy as np

import main_count
import distance_btw_add as dba
import add_value_pairs as avp
import key_val as kv
import key_generator as keygen
import feature_dictionary
import feature_file as ff
import best_address_pair as rfba
import time
from encoder import charName

current_time = lambda: int(round(time.time()))

'''
This function returns the naive features
'''
def generateFeatureDictionary(addresskeys,keyAddressCounts):
	logger.info("generating feature list")
	featurelist = defaultdict(list)
	
	for keypressed in keyAddressCounts:
		for key in addresskeys:
			if key in keyAddressCounts[keypressed]:
				featurelist[key].append(keyAddressCounts[keypressed][key])
			else:
				#featurelist[key].append(np.NaN)
				featurelist[key].append('NaN')
		#print('neupane',keypressed.split('_')[0])
		featurelist['class'].append(charName(keypressed.split('_')[0]))
	logger.debug("featurelist length %d",len(featurelist))
	#print(featurelist)
	return featurelist


def main(a_log_folder):
	
	#a_log_folder = 'test'
	library_path = '../data/'+a_log_folder
	
	log_files = os.listdir(library_path)
	add_key_list = avp.add_value() #initialize address book, and data dictionary
	logger.debug('extracting features')
	for a_log_file in log_files:
		input_file = library_path+"/"+a_log_file
		statinfo = os.stat(input_file)
		if statinfo.st_size !=0:
			#Initialize key_val object to store keys, values, and beginning point of each address
			logger.debug('library %s',a_log_file)
			key_val=kv.key_val()

			with open(input_file, 'r') as csvfile:
				csv_reader = csv.reader(csvfile, delimiter='\t', quotechar='|')
				for row in csv_reader:			
					key_val.set_keys_val_list('_'.join((row[1].split('/')[-1]).split(',')),int(row[0])) #add_key,values	

			print('running dba_distance')
			dba_distance=dba.distance_btw_add(key_val,add_key_list)
			print('setting feature vector')
			key_gen=keygen.key_generator(input_file)
			add_key_list.set_feature_per_key(key_gen.get_key(),dba_distance.get_differences())

	featurelist=generateFeatureDictionary(add_key_list.get_address_keys(),add_key_list.get_feature_per_key())
	if not os.path.exists('../feature_diff/'):
		os.makedirs('../feature_diff/')
	fe_ff = ff.feature_file('../feature_diff/feature_'+a_log_folder+'.csv',featurelist)
	fe_ff.generateFeatureFile()
	

#log_folders = ['libskia_ftrace_2','libskia_ftrace_CapitolOne'] #name of the folder with log files
log_folders = ['try']
for a_log_folder in log_folders:
	#main_count.count_addresses(a_log_folder)
	main(a_log_folder)
	rfba.feature_ranking()

