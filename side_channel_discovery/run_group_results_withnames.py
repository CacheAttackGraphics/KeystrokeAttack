import pandas as pd
from collections import defaultdict
import csv

position_value = ['0','1','2','3','4','5','6','7','8','9','a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z']

name_maybe = ['zero','one','two','three','four','five','six','seven','eight','nine']
name_list = ['0','1','2','3','4','5','6','7','8','9']
def main():
	distribution_list = defaultdict(set)
	csvfile = open('../results/distribution_kstar.csv','r')
	count = 0
	pred_prob = 0
	for rows in csvfile:
		if count > 0:
			values = rows.split(',')

			for value in values[4:]:
				try:
					pred_prob = round(float((value.split('*')[1]).strip('\n'))*100,2)
				except:
					pred_prob = round(float(value.strip('\n'))*100,2)

				if int(pred_prob) > 0:
					try:
						distribution_list[name_list[name_maybe.index(values[1].split(':')[1])]].add(position_value[values.index(value)-4])
					except:
						distribution_list[values[1].split(':')[1]].add(position_value[values.index(value)-4])
		count+=1
	#print(distribution_list)

	with open('../results/dict.csv', 'w',newline='') as csv_file:
		writer = csv.writer(csv_file)
		for key, value in distribution_list.items():
		   writer.writerow([key, value])

	groups_all = defaultdict(list)
	flag = False
	for key,value in distribution_list.items():
		if groups_all:
			for main_key in groups_all:
				print(main_key,groups_all)
				if key in groups_all[main_key] or main_key in value:
					groups_all[main_key].append(value)
					falg = True
			if flag == False:
				groups_all[key].append(value)
				flag = False
		else:
			groups_all[key].append(value)


	with open('../results/dict_main_grp.csv', 'w',newline='') as csv_file:
		writer = csv.writer(csv_file)
		for key, value in groups_all.items():
		   writer.writerow([key, value])
	
main()


