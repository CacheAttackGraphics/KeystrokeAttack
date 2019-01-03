import pandas as pd
import numpy as np
from matplotlib import pyplot as plt
from encoder import charName

from classification_engine import preparefile

data_numbers= ['0','1','2','3','4','5','6','7','8','9','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z']

#remove outliers for each class
def remove_each_outlier(df):

	grouped=df.groupby('class')
	#df = df[np.abs(df.measurement-df.measurement.mean()) <= (3*df.measurement.std())]
	#df = df[np.abs(df.measurement_2-df.measurement_2.mean()) <= (3*df.measurement_2.std())]
	#return df
	df = grouped.apply(lambda g: g[ abs(g['measurement'] - g['measurement'].mean()) <= (3*g['measurement'].std())])
	#df = df.apply(lambda g: g[ abs(g['measurement_2'] - g['measurement_2'].mean()) <= (3*g['measurement_2'].std())])
	return df 

#Validating classification as training and testing set
def two_main_traini_test():

	#data_characters=['a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z']
	df = pd.read_csv(filetype+'.txt',names=['class','measurement','measurement_2','diff_1','diff_2'],sep=r"\s*")
	testing_data = df[['measurement','measurement_2','class']]
	testing_data=testing_data.rename(index=str, columns={"measurement": "ground_truth"})
	#testing_data = testing_data[testing_data['class'].isin(data_numbers)]
	testing_data['class']=testing_data['class'].apply(charName)
	print(testing_data.head())
	testing_data_write=testing_data[['ground_truth','class']]
	testing_data= testing_data[testing_data.ground_truth != 0]
	#testing_data=testing_data[testing_data.ground_truth_2!=0]

	testing_data_write.to_csv('testing_mod_new.csv',index=False)
	
	training_data = df[['measurement_2','class']]
	training_data=training_data.rename(index=str, columns={"measurement_2":"ground_truth"})
	#training_data = training_data[training_data['class'].isin(data_numbers)]
	training_data['class']=training_data['class'].apply(charName)
	training_data= training_data[training_data.ground_truth != 0]
	#training_data= training_data[training_data.ground_truth_2!= 0]

	training_data.to_csv('training_mod_new.csv',index=False)

#used for android
def one_measurement_main():
	#data_characters=['a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z']
	df = pd.read_csv(filetype+'.txt',names=['class','measurement'],sep=r"\s*")
	df = remove_each_outlier(df)
	testing_data = df[['measurement','class']]
	testing_data['class']=testing_data['class'].apply(charName)
	testing_data=   testing_data[testing_data.measurement != 0]
	testing_data.to_csv(filetype+'.csv',index=False)


#Used for Android CapitalOne
def two_measurements_main():
	#data_characters=['a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z']
	df = pd.read_csv(filetype+'.txt',names=['class','measurement','measurement_2'],sep=r"\s*")
	df = remove_each_outlier(df)
	testing_data = df[['measurement','measurement_2','class']]
	testing_data['class']=testing_data['class'].apply(charName)
	testing_data=   testing_data[testing_data.measurement_2 != 0]
	testing_data=   testing_data[testing_data.measurement != 0]
	print(testing_data.head())
	testing_data.to_csv(filetype+'.csv',index=False)

#Used for 1 feature Pin
def one_feature_pin():
	#data_characters=['a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z']
	df = pd.read_csv(filetype+'.txt',names=['class_type','measurement','measurement_2'],sep=r"\s*")
	df = df[df['class_type'].isin(['1','2','3','4','5','6','7','8','9','0'])]
	print(df.head())
	df = df[['measurement','measurement_2','class_type']]
	df['class_type']=df['class_type'].apply(charName)
	testing_data=   df[df.measurement != 0]
	testing_data=   testing_data[testing_data.measurement_2 != 0]

	df_reorder = testing_data[['class_type','measurement','measurement_2']] # rearrange column here
	df_reorder.to_csv(filetype+'.csv',index=False)


#if there are two features in your file __ used for onboard ubuntu
def two_feature_main():

	class_list = ['1','2','3','4','5','6','7','8','9','0']
	#data_characters=['a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z']
	df = pd.read_csv(filetype+'.txt',names=['class_type','measurement','measurement_2','measurement_3','measurement_4'],sep=r"\s*")
	df = df[['measurement','measurement_2','measurement_3','measurement_4','class_type']]

	df['class_type']=df['class_type'].apply(charName)
	testing_data=   df[df.measurement != 0]
	testing_data['class_type']=testing_data['class_type'].apply(charName)
	testing_data=   testing_data[testing_data.measurement_2 != 0]
	testing_data=   testing_data[testing_data.measurement_3 != 0]
	testing_data=   testing_data[testing_data.measurement_4 != 0]

	print(testing_data.head())
	df_reorder = testing_data[['class_type','measurement','measurement_2','measurement_3','measurement_4']] # rearrange column here
	df_reorder.to_csv(filetype+'.csv',index=False)



#Your measurement data should be in format of result_CapitalOne_merged
filetype = "../data/online_profiling/result_CapitalOne_merged"
#Call appropriate function for Ubuntu or Android
two_measurements_main()
preparefile(filetype+".csv")

