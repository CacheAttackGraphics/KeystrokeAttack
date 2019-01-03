import pandas as pd
import numpy as np
from matplotlib import pyplot as plt
from encoder import charName

from classification_engine import run_classifiers
from plot_graph import plot_address

data_numbers= ['0','1','2','3','4','5','6','7','8','9','a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z']

offset_dict = {'zero': 13352.25,
'one': 8390.5,
'two': 7962.0,
'three': 11674.25,
'four': 11293.75,
'five': 13856.75,
'six': 10697.0,
'seven': 8297.75,
'eight': 13705.75,
'nine': 13499.0,
'a': 18420.25,
'b': 17101.25,
'c': 15203.25,
'd': 15237.0,
'e': 17575.75,
'f': 12580.0,
'g': 17810.5,
'h': 13400.5,
'i': 11390.75,
'j': 13682.0,
'k': 13051.75,
'l': 16431.75,
'm': 4820.5,
'n': 9221.5,
'o': 8530.25,
'p': 12199.5,
'q': 7724.5,
'r': 19370.25,
's': 8880.5,
't': 4558.5,
'u': 15360.75,
'v': 14877.0,
'w': 6894.0,
'x': 14435.5,
'y': 15349.5,
'z': 9437.5
}

class lineoffit(object):

	def __init__(self,x,y):
		self.x = x
		self.y = y
		self.lof={}

	def line_of_fit(self):
		m, b = np.polyfit(self.x, self.y, 1)
		self.lof[m]=m
		self.lof[b]=b
		return self.lof



class outliers(object):
	def __init__(self,df):
		self.df = df

	def preprocess_outlier(self,data_numbers):
		gb = self.df.groupby('class')
		for value in data_numbers:
			#print('ajaya',df['class'],'***********************',value)
			#data = df['ground_truth'].loc[df['class'] == value]
			#print(gb)
			data = gb.get_group(value)
			#print(data['ground_truth'])
			rmo=outliers(data['ground_truth'])
			temp_df=pd.DataFrame(rmo.remove_outliers())
			#print("neupane",temp_df.head())
			temp_df['class']=charName(value)
			#print('ajaya',temp_df['class'])
			df_list.append(temp_df)
		print(df.head())
		df_all = pd.concat(df_list,axis=0)
		return df_all
	
	def remove_outliers(self):
		#df = df.drop(df.std()[(df.std() < int(threshold1))].index, axis=1)
		#print(self.df.values)
		y = self.df.values
		y=y.astype(np.float)
		#print(y.mean())
		return self.df[np.abs(y-y.mean())<=(y.std())] #keep only the ones that are within +3 to -3 standard deviations in the column 'Data'.

def one_testing():
	df_list = []
	count_zero = 0

	#data_characters=['a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z']
	df = pd.read_csv('../measurements/result_gedit_nomod.txt',names=['class','measurement'],sep=r"\s*")
	testing_data = df[['measurement','class']]
	testing_data=testing_data.rename(index=str, columns={"measurement": "ground_truth"})
	testing_data = testing_data[testing_data['class'].isin(data_numbers)]


	testing_data['class']=testing_data['class'].apply(charName)
	testing_data= testing_data[testing_data.ground_truth != 0]

	testing_data.to_csv('../mldata/testing_nonmod_gedit.csv',index=False)


def one_main():
	df_list = []
	count_zero = 0

	#data_characters=['a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z']
	df = pd.read_csv('../measurements/result_gedit_mod.txt',names=['class','measurement','ground_truth'],sep=r"\s*")
	testing_data = df[['measurement','class']]
	testing_data=testing_data.rename(index=str, columns={"measurement": "ground_truth"})
	testing_data = testing_data[testing_data['class'].isin(data_numbers)]
	testing_data['class']=testing_data['class'].apply(charName)
	testing_data= testing_data[testing_data.ground_truth != 0]

	testing_data.to_csv('../mldata/testing_gedit.csv',index=False)
	
	training_data = df[['ground_truth','class']]
	training_data = training_data[training_data['class'].isin(data_numbers)]
	training_data['class']=training_data['class'].apply(charName)
	training_data.to_csv('../mldata/training_gedit.csv',index=False)


def main_testing():
	#data_characters=['a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z']
	df = pd.read_csv('../measurements/new/result_onboard_nomod.txt',names=['class','measurement','measurement_2'],sep=r"\s*")
	testing_data = df[['measurement','measurement_2','class']]
	testing_data=testing_data.rename(index=str, columns={"measurement": "ground_truth","measurement_2":"ground_truth_2"})
	testing_data = testing_data[testing_data['class'].isin(data_numbers)]
	testing_data= testing_data[testing_data.ground_truth != 0]
	testing_data=testing_data[testing_data.ground_truth_2!=0]
	

	testing_data['class']= testing_data['class'].apply(charName)
	print(testing_data.head())


	testing_data.to_csv('../mldata/testing_non_mod_new.csv',index=False)

	calcoffset()

def calcoffset():

	csvreader = open('../mldata/testing_non_mod_new.csv','r')
	csvwriter = open('../mldata/testing_non_mod_new_with_offset.csv','w')

	count = 0
	for rows in csvreader:
		values = rows.strip('\n').split(',')
		if count == 0:
			csvwriter.write(values[0]+','+values[1]+','+values[2]+'\n')
			count = 1
		else:
			y = values[2]
			x = int(values[0]) + int(offset_dict[str(y)])
			z = int(values[1]) + int(offset_dict[str(y)])
			csvwriter.write(str(x)+','+str(z)+','+y)
			csvwriter.write('\n')
	csvwriter.close()

	#print(testing_data)
	# for column in range(0,testing_data.shape[0]):
	# 	print('ajaya',testing_data.shape[0],column)
	# 	print('neup',testing_data.iloc[[column]])
	# 	#print(testing_data.iloc[column]- offset_dict[testing_data.loc[testing_data['class']]])
	# 	y = testing_data.iloc[column]['class']
	# 	#print(y)
	# 	testing_data.iloc[column]['ground_truth']== int(testing_data.iloc[column]['ground_truth'])- int(offset_dict[str(y)])
	# 	testing_data.iloc[column]['ground_truth_2']== int(testing_data.iloc[column]['ground_truth_2'])- int(offset_dict[str(y)])


def main():

	#data_characters=['a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z']
	df = pd.read_csv('../measurements/new/result_onboard_mod.txt',names=['class','measurement','measurement_2','ground_truth','ground_truth_2'],sep=r"\s*")
	testing_data = df[['measurement','measurement_2','class']]
	testing_data=testing_data.rename(index=str, columns={"measurement": "ground_truth","measurement_2":"ground_truth_2"})
	testing_data = testing_data[testing_data['class'].isin(data_numbers)]
	testing_data['class']=testing_data['class'].apply(charName)
	print(testing_data.head())
	testing_data= testing_data[testing_data.ground_truth != 0]
	testing_data=testing_data[testing_data.ground_truth_2!=0]


	testing_data.to_csv('../mldata/testing_mod_new.csv',index=False)
	
	training_data = df[['ground_truth','ground_truth_2','class']]
	training_data = training_data[training_data['class'].isin(data_numbers)]
	training_data['class']=training_data['class'].apply(charName)
	training_data= training_data[training_data.ground_truth != 0]
	training_data= training_data[training_data.ground_truth_2!= 0]

	training_data.to_csv('../mldata/training_mod_new.csv',index=False)

	
main_testing()



