#length of the password: n
#possible guesses in each position: k (calculated based on the probability distribution obtained from the classifier)
#fix the positions with the highest probability first (this can be the improvement on the number of guesses)--to be implement afterwards
#pick the possible words from the dictionary
#match the perfect guess, return the number of guesses -- This is for the ground truth. 
#worst case will be the number of combinations of characters
#brute force is 26^8

import pandas as pd
from collections import defaultdict
#from dict_search_rnd import dict_search
from random import randint
from encoder import charName
from math import pow

from encoder import _reverse

symbols = ['?','#','*','.','&','-','+','_','!','\\']
names = ['inst#','actual','pred','error','zero','six','seven','q','w','e','r','t','y','u','i','p','a','s','d','f','g','h','j','k','l','m','one','two','three','five','eight','nine','z','x','c','v','b','n','four','o']
#names=['inst#','actual','pred','error','zero','one','two','three','four','five','six','seven','eight','nine','a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z']
filename = "passwd_10k.txt"

#This function returns the list of passwords I want to break
def generateRandomWords():
	words = []
	with open(filename, 'r') as fp:
		rows = fp.readlines()
		for a_row in rows:
			flag = True
			for a_char in a_row:
				if a_char in symbols:
			 		flag = False 
			if flag == True:
				words.append(a_row.strip())
	#print(words)
	return words

def append_rem_values(list_guesses):
	print(list_guesses)
	for x in names[4:]:
		if x not in list_guesses:
			list_guesses.append((x,0))
	#print(list_guesses)
	return list_guesses

#This function gives the predicted key and the corresponding weight
def list_of_guesses(filename):
	org_key = []
	keys_list = defaultdict(list)
	read_file = open(filename,'r')
	count=0
	for lines in read_file:
		if count>0 and lines != "\n" :
			values =  lines.strip("\n").split(',')
			#print(values)
			org_key.append(values[1].split(':')[1])
			pos_keys = []
			for pos,each_value in enumerate(values[4:]):
				#print(pos,each_value,names[pos+14])
				if each_value !='0':
					if '*' in each_value:
						each_value=float(each_value[1:])
					pos_keys.append((names[pos+4],each_value))
			keys_list[values[1].split(':')[1]].append(pos_keys)
		count+=1

	keys_list = append_keys(keys_list)
	#print_len(keys_list)
	#print(keys_list)
	return keys_list


count = 0
found = 0

#This function ranks the list as per the majority voiting.
def append_keys(keys_list):
	new_key_list = defaultdict()
	for keys in keys_list:
		x = []
		dict_count = defaultdict(int)
		count_list = 0
		for key in keys_list[keys]:
			if count_list < 10:
				for anelement,confidence in key:
					dict_count[anelement]+=1*float(confidence)
					x.append(_reverse(anelement))
			count_list+=1
		print(dict_count)
		
		#This is to append extra keys for only 1 case
		for val in names[4:]:
			if val not in list(dict_count.keys()):
				dict_count[val]=0

		x = list(dict_count.keys())
		x.sort(key=lambda i: dict_count[i],reverse=True)

		new_key_list[keys] = x
	return new_key_list


def print_len(new_key_list):

	for keys in new_key_list:
		print(len(new_key_list[keys]),new_key_list[keys])


keys = []

words = generateRandomWords()

#train_distribution = 'distribution_training.csv'
#training_guesses = list_of_guesses(train_distribution)
test_distribution = 'distribution/distribution_test.csv'
test_guesses = list_of_guesses(test_distribution)

#print(training_guesses)
#print(test_guesses)
file_out = open('results_modeled_with_confidence_avg.csv','w')
word_given = ""
for p_word in words:
	p_word = p_word.lower()
	print("***************************")
	print(p_word)
	keys = []
	for a_char in p_word:
		print(a_char)
		keys.append(test_guesses[charName(a_char)])	#if you turn on append

	
	print(keys)
	x = [ keys[i].index(charName(p_word[i])) for i in range(len(p_word))]
	print(x)
	ret = 0

	#file_out = open('results_modeled_with_confidence_dfs.csv','w')
	# for i in range(len(p_word)):
	# 	z = 1
	# 	for j in range(i+1,len(p_word)):
	# 		z = z * len(keys[j])
	# 	ret += x[i] * z

	#file_out = open('results_modeled_with_confidence_pow.csv','w')
	#ret = pow(max(x)+1,len(p_word))

	ret = (pow(max(x)+1,len(p_word)) + pow(max(x),len(p_word)) + 1.0) / 2
	file_out.write(p_word.lower()+","+str(ret)+"\n")



