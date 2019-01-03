__author__ = 'Ajaya Neupane'
import os
from collections import defaultdict 
import logging
import csv
from encoder import charName
import itertools
import key_generator
import check_noise_threshold
from collections import Counter

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)
import time

current_time = lambda: int(round(time.time()))

class distance_btw_add(object):

	def __init__(self,key_val,add_key_list):
		self.key_val=key_val
		self.add_key_list=add_key_list


	def get_differences(self):
		keys = self.key_val.get_keys_list() #get all the keys
		#print(keys)
		values=self.key_val.get_val_list()  #get all the values
		#count_dict=Counter(keys)
		add_begin_pos_dict= self.key_val.get_add_begin_pos_dict() #store beginning of each address
		key_diff_dict = {} #all features
		count = 0

		for key1,key2 in itertools.combinations(set(keys), 2):
			first_key_pos = keys.index(key1)
			second_key_pos = keys.index(key2)
			if second_key_pos > first_key_pos:
				dict_key= str(key1)+"_"+str(key2)
				key_diff_dict[dict_key]=add_begin_pos_dict[key2]- add_begin_pos_dict[key1]

			else:
				dict_key=str(key2)+"_"+str(key1)
				key_diff_dict[dict_key]=add_begin_pos_dict[key1]- add_begin_pos_dict[key2]
			
			self.add_key_list.set_address_keys(dict_key)

		return key_diff_dict