import pandas as pd
import numpy as np
from matplotlib import pyplot as plt
from encoder import charName

from classification_engine import run_classifiers
from plot_graph import plot_address


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



def main():
	df_list = []
	data_numbers= ['0','1','2','3','4','5','6','7','8','9','a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z']
	#data_characters=['a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z']
	df = pd.read_csv('../results/result_0xe3e_libft2.so_0xbcf3_libskia.so.txt',names=['class','measurement','ground_truth'],sep=r"\s*")
	testing_data = df[['measurement','class']]
	testing_data=testing_data.rename(index=str, columns={"measurement": "ground_truth"})
	testing_data = testing_data[testing_data['class'].isin(data_numbers)]
	testing_data['class']=testing_data['class'].apply(charName)
	print(testing_data.ground_truth == 0)
	testing_data= testing_data[testing_data.ground_truth != 0]
	print(testing_data.head())

	testing_data.to_csv('../results/testing_gedit_10.csv',index=False)
	
	
main()



