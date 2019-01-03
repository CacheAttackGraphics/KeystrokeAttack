import pandas as pd
import numpy as np
import os
import time
import sys


threshold = 1000

def remove_multiple_zeros(df):
	grouped = df.groupby('class')
	print(grouped.groups)

def filter_feature_sd(feature_file):
	df = pd.read_csv(feature_file)

	if not os.path.exists('../feature_filtered/'):
	    os.makedirs('../feature_filtered/')
	#remove_multiple_zeros(df)
	df.dropna(axis=1, inplace=True)
	#df.to_csv("../feature_filtered/filtered_wo_nan"+feature_file.split('/')[-1],index=False)
	df.drop(df.std()[(df.std() == 0)].index, axis=1,inplace=True)
	df.drop(df.std()[(df.std() < int(threshold))].index, axis=1,inplace=True)
	df.to_csv("../feature_filtered/filtered_"+feature_file.split('/')[-1],index=False)
