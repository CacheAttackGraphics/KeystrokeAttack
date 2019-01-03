__author__ = 'Ajaya Neupane'
import os
from collections import defaultdict
import logging
import csv
from encoder import charName

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)


#split at the first occurrence
def keyGenerator(filename):

	return str(filename).split('.',1)[0]

def generateDicts(addresskeys,filename):
	#logger.info("generating list of addresses for keys")
	key_count_dict = defaultdict(int)
	address_keys=set()
	pagedict = defaultdict(list)
	local_address_keys = set()

	with open(filename, 'r') as csvfile:
		csv_reader = csv.reader(csvfile, delimiter='\t', quotechar='|')
		for enk,row in enumerate(csv_reader):
			if '.dll' not in row[0]:
				#print(enk)
				add_key,value = row[1],int(row[0])
				key_count_dict[add_key]+=1
				addresskeys.add(add_key)

	return key_count_dict

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
				featurelist[key].append(0)
		featurelist['class'].append(charName(keypressed.split('_')[0]))

	#print featurelist['0x1f37']
	logger.debug("featurelist length %d",len(featurelist))

	return featurelist


"""
This function generates feature file to be used with sklearn or weka for machine learning. 
"""
def generateFeatureFile(filename,featurelist):
	keys = sorted(featurelist.keys())
	with open(filename, "w", newline='') as outfile:
		writer = csv.writer(outfile, delimiter = ",")
		writer.writerow(keys)
		writer.writerows(zip(*[featurelist[key] for key in keys]))

	logger.info("CSV FILE GENERATED!!!")

'''
The task of this function is to generate a .csv file 
with each column heading as address, 
and each row as the count number of address calls for every key press event
'''
def count_addresses(a_log_folder):

	library_path = '../data/'+a_log_folder
	log_files = os.listdir(library_path)
		
	all_data = defaultdict(list)
	address_keys = set()
	
	for a_log_file in log_files:
		logger.debug('library %s',a_log_file)
		input_file = library_path+"/"+a_log_file
		statinfo = os.stat(input_file)
		if statinfo.st_size !=0:
			logger.debug(a_log_file)
			key_count_dict = generateDicts(address_keys,input_file)
			all_data[keyGenerator(a_log_file)] = key_count_dict

	logger.debug('number of unique keys %d', len(address_keys))

	featurelist=generateFeatureDictionary(address_keys,all_data)
	if not os.path.exists('../feature_count/'):
		os.makedirs('../feature_count/')
	generateFeatureFile('../feature_count/'+a_log_folder+'_feature_count.csv',featurelist)

#count_addresses()