import pandas as pd
from collections import defaultdict
import csv

def sort_results_sorry():

	distribution_list = defaultdict(set)
	csvfile = pd.read_csv('../results/distribution.csv',names=['inst#','actual','predicted','error','zero','one','two','three','four','five','six','seven','eight','nine','a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z'],skiprows=1,delimiter=',')
	
	column_names = csvfile.columns 
	#print(column_names)

	for row_no in range(csvfile.shape[0]):
		if csvfile.loc[row_no]['error']=='+':
			actual=(csvfile.loc[row_no]['actual']).split(':')[1]
			#print(sorted(csvfile.loc[row_no][4:]))

def sort_results():
	distribution_list = []
	csvfile = open('../results/distribution.csv','r')
	count = 0
	for rows in csvfile:
		
		if count > 0 and len(rows.split(','))>1:
			line = []
			values = rows.split(',')
			#print(values)
			line.append(values[0].strip())
			line.append(values[1].strip())
			line.append(values[2].strip())
			line.append(values[3].strip())

			for value in values[4:]:
				try:
						line.append(round(float((value.split('*')[1]).strip('\n'))*100,2))
						#print("inside try",round(float((value.split('*')[1]).strip('\n'))*100,2))		
				except:
					line.append(round(float(value.strip('\n'))*100,2))
		
			distribution_list.append(line)
		count+=1
	find_probability_map(distribution_list)

def find_probability_map(distribution_list):
	correct_ans=0
	index_list =['zero','one','two','three','four','five','six','seven','eight','nine','a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z']
	updated_list = []
	for row in distribution_list:
		if row[3] == '+':
			#print(row[3])
			wrong_row = []
			wrong_row.append(row[1].split(':')[1]+':')
			#wrong_row.append(row[2].split(':')[1]+':')
			predictons=row[4:]
			all_predictions = sorted([i for i in row[4:] if i > 0.0],reverse=True)
			indices = []
			done_list = []
			for guess in all_predictions:
				if guess not in done_list:
					indices += [i for i, x in enumerate(predictons) if x == guess]
					done_list.append(guess)

			for aindex in indices:
				wrong_row.append(index_list[aindex]) 	
			updated_list.append(wrong_row)
		else:
			correct_ans+=1

	write_csv(updated_list,correct_ans)


def calc_pred_improvement(correct_ans):
	count=0
	output_file = open('../results/ranked_guesses.csv','r')
	all_data=0
	how_many_guesses = 4
	guess_list_dict = {}
	guess_list = [0] * how_many_guesses
	for arow in output_file:
		#print(arow)
		pred = (arow.strip()).split(',')
		ind = 0
		if pred[0].split(':')[0] in guess_list_dict:
			guesses = guess_list_dict[pred[0].split(':')[0]]
		else:
			guesses = [0] * how_many_guesses

		for aval in pred[1:how_many_guesses+1]:
			if aval == pred[0].split(':')[0]:
				guesses[ind]+=1
				guess_list[ind]+=1
				count+=1
				print('hit')
			else:
				print(aval,pred[0],'miss')
			ind+=1
		guess_list_dict[pred[0].split(':')[0]]=guesses
		all_data+=1

	overall_acc = round(float(correct_ans/(all_data+correct_ans)),4)
	increment = round(float(count/(all_data+correct_ans)),4)

	#output_guess_level = open('../results/increment.csv','w',newline='')

	#output_guess_level.write('Name,first,second,third,fourth\n')

	print(guess_list_dict)
	print('First Guess,Second Guess,Third Guess, Fourth GUess, ....')
	print(round(float(guess_list[0]/(all_data+correct_ans)),4),round(float(sum(guess_list[0:2])/(all_data+correct_ans)),4),round(float(sum(guess_list[0:3])/(all_data+correct_ans)),4),round(float(sum(guess_list[0:4])/(all_data+correct_ans)),4),increment,overall_acc,count,all_data,correct_ans)

def write_csv(updated_list,correct_ans):
	output = open('../results/ranked_guesses.csv','w',newline='')
	writecsv = csv.writer(output)
	for arow in updated_list:
		writecsv.writerow(arow)
	output.close()
	calc_pred_improvement(correct_ans)

def main():
	distribution_list = defaultdict(set)
	csvfile = open('../results/distribution_kstar.csv','r')
	count = 0
	unsuccessful=0
	for rows in csvfile:
		if count > 0:
			values = rows.split(',')
			for value in values[4:]:
				if value.strip() != '0':
					#print(count,value)
					try:
						if float((value.split('*')[1]).strip('\n'))*100 > 1:
							distribution_list[values[1].split(':')[1]].add(values.index(value)-4)
						else:
							unsuccessful+=0
					except:
						#print(value)
						if float(value.strip('\n'))*100 > 1:
							#print('with star',count,value)
							distribution_list[values[1].split(':')[1]].add(values.index(value)-4)
						else:
							unsuccessful+=0
		count+=1
	print(count,unsuccessful)

	with open('../results/dict.csv', 'w',newline='') as csv_file:
		writer = csv.writer(csv_file)
		for key, value in distribution_list.items():
		   writer.writerow([key, value])

sort_results()
#calc_pred_improvement()

