
import numpy as np
import pandas as pd
import sys,os
from collections import defaultdict
#test data
from sklearn.datasets import load_iris

#preprocessing
from sklearn import preprocessing

#feature selection

from sklearn.feature_selection import VarianceThreshold
from sklearn.feature_selection import SelectKBest,chi2,mutual_info_classif
from sklearn.feature_selection import f_regression
from sklearn.pipeline import Pipeline
from sklearn.feature_selection import SelectPercentile, f_classif

from sklearn.feature_selection import RFE
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import ExtraTreesClassifier
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def feature_importance(X,y):
	# feature extraction
	forest = ExtraTreesClassifier()
	forest.fit(X, y)
	importances = forest.feature_importances_
	std = np.std([tree.feature_importances_ for tree in forest.estimators_],
				 axis=0)
	indices = np.argsort(importances)[::-1]
	newlist = []  #list of all addresses ranked
	# Print the feature ranking
	print("Feature ranking:")

	for f in range(X.shape[1]):
		newlist.append((X.columns[f], importances[indices[f]]))

	print(newlist[:3])
	return newlist[:3]
	
def recursive_feature_elimination(X,y):
	# feature extraction
	model = LogisticRegression()
	rfe = RFE(model, 3)
	selected_features = rfe.fit(X, y)
	indices_selected = selected_features.get_support(indices=True)
	colnames_selected = [X.columns[i] for i in indices_selected]

	print(colnames_selected)

	X_new = X[colnames_selected]
	
	frames=[X_new,y]
	pf=pd.concat(frames,axis=1)

	return pf,X_new

#Remove if some address appears multiple times. 
def remove_dup(colnames_selected):
	sel_cols = []
	add_occ= defaultdict(int)
	for x in colnames_selected:
		print(x)
		add_occ[x[:10]]+=1
		for y in colnames_selected:
			if x[:10] in y and add_occ[x[:10]]<=3:
				sel_cols.append(y)
				add_occ[x[:10]]+=1
	return sel_cols

#selecting the best features based on univariate statistical tests
def remove_features_on_univariate_selection(X,y):
	selected_features=SelectKBest(mutual_info_classif, k=100).fit(X, y)
	indices_selected = selected_features.get_support(indices=True)
	colnames_selected = [X.columns[i] for i in indices_selected]
	#colnames_selected = remove_dup(colnames_selected)
	X_new = X[colnames_selected]
	frames=[X_new,y]
	pf=pd.concat(frames,axis=1)
	return pf,X_new,colnames_selected


def remove_features_with_low_variance(X,y):

	selected_features = VarianceThreshold(threshold=(.8 * (1 - .8))).fit(X)
	indices_selected = selected_features.get_support(indices=True)
	colnames_selected = [X.columns[i] for i in indices_selected]

	print(colnames_selected)

	X_new = X[colnames_selected]
	
	frames=[X_new,y]
	pf=pd.concat(frames,axis=1)

	return pf,X_new


def selected_features(data_X,target_y):
	#return remove_features_with_low_variance(data_X)
	#feature_importance(data_X,target_y)
	#recursive_feature_elimination(data_X,target_y)
	return remove_features_on_univariate_selection(data_X,target_y)