from collections import defaultdict
import time
import numpy as np
import pandas as pd
import sys,os
import re
import csv
from matplotlib import pyplot as plt

#model selection
from sklearn.model_selection import cross_val_score, cross_val_predict,KFold
from sklearn import metrics
from sklearn.model_selection import train_test_split
from sklearn.model_selection import LeaveOneOut
from sklearn.metrics import classification_report
from sklearn.metrics import accuracy_score, precision_recall_fscore_support
from sklearn.metrics import accuracy_score
from sklearn.metrics import confusion_matrix

#Classifiers
from sklearn.naive_bayes import GaussianNB
from sklearn.svm import SVC
from sklearn.svm import LinearSVC
from sklearn.linear_model import LogisticRegression
from sklearn.neighbors import KNeighborsClassifier
from sklearn import tree
from sklearn.ensemble import RandomForestClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.discriminant_analysis import LinearDiscriminantAnalysis
from sklearn.neural_network import MLPClassifier
from xgboost import XGBClassifier

path=""


def train_test_classification(model, X, y):
	# create training and testing vars
	X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.4)
	frames = [X_train,y_train]
	df = pd.concat(frames,axis=1)
	X_train = df.iloc[:,0:-1]
	y_train = df.iloc[:,-1]
	genmodel = model.fit(X_train, y_train)
	
	# predict
	y_pred = genmodel.predict(X_test)
	results = genmodel.predict_proba(X_test)[0]
	# gets a dictionary of {'class_name': probability}
	prob_per_class_dictionary = dict(zip(genmodel.classes_, results))
	# gets a list of ['most_probable_class', 'second_most_probable_class', ..., 'least_class']
	results_ordered_by_probability = map(lambda x: x[0], sorted(zip(genmodel.classes_, results), key=lambda x: x[1], reverse=True))
	#for a_result in results_ordered_by_probability:
	#	print(a_result,results_ordered_by_probability[a_result])
	
	print(classification_report(y_test, y_pred))
	return accuracy_score(y_test, y_pred)

#if you have multiple features you can use random forest feature selection.
def random_forest_feature_selection(data_X,target_y):

	# Create a random forest classifier
	clf = RandomForestClassifier(bootstrap=True, class_weight=None, criterion='gini',
            max_depth=None, max_features='auto', max_leaf_nodes=None,min_samples_leaf=1,
            min_samples_split=2, min_weight_fraction_leaf=0.0,
            n_estimators=100, n_jobs=-1, oob_score=False, random_state=0,
            verbose=0, warm_start=False)

	feat_labels = list(data_X.columns.values)
	# Train the classifier
	clf.fit(data_X, target_y)

	# Print the name and gini importance of each feature
	for feature in zip(feat_labels, clf.feature_importances_):
	    print(feature)

	X_train, X_test, y_train, y_test = train_test_split(data_X, target_y, test_size=0.3)

	genmodel = clf.fit(X_train, y_train)
	# predict
	y_pred = genmodel.predict(X_test)

	print(classification_report(y_test, y_pred))
	return accuracy_score(y_test, y_pred)

#get cross validation report
def cross_fold_validation(model, data_X, target_y,name):
	seed = 0
	cv_report = cross_val_score(model, data_X, target_y, cv=10)
	target_y_pred = cross_val_predict(model, data_X, target_y, cv=10)
	report = classification_report(target_y, target_y_pred)
	print(confusion_matrix(target_y, target_y_pred))
	print(report)
	classifaction_report_csv(report,name)
	return cv_report

#Crossvalidation to test the strength of the model
def run_ten_fold_classifiers(data_X,target_y):
		
		# prepare models
		models = []
		models.append(('KNN', KNeighborsClassifier(n_neighbors=1)))
		models.append(('RandomForest', RandomForestClassifier(n_estimators=100)))
		
		# evaluate each model in turn
		results = []
		results_loo = []
		names = []
		for name, model in models:
			cv_results = cross_fold_validation(model, data_X, target_y,name)
			results.append(cv_results)
			names.append(name)
			msg = "%s: %f (%f)" % (name, cv_results.mean(), cv_results.std())
			print(msg)


def generateFeatureFile(classes,featurelist):
	with open('results_new.csv', "w", newline='') as outfile:
		writer = csv.writer(outfile, delimiter = ",")
		writer.writerows(zip(classes,featurelist))


def classifaction_report_csv(report,modeltype):
	report_data = []
	lines = report.split('\n')
	for line in lines[2:-3]:
		row_data = re.split('\s+', line.strip())
		#print(row_data)
		row = {}
		row['class'] = row_data[0]
		row['precision'] = float(row_data[1])
		row['recall'] = float(row_data[2])
		row['f1_score'] = float(row_data[3])
		row['support'] = float(row_data[4])
		report_data.append(row)
	dataframe = pd.DataFrame.from_dict(report_data)
	print("**************",path)
	dataframe.to_csv(path + '/classification_report'+modeltype+'.csv', index = False)

def run_classifiers(X,y):		
		# prepare models
		models = []
		#models.append(('KNN', KNeighborsClassifier(n_neighbors=3)))
		models.append(('RandomForest', RandomForestClassifier(bootstrap=True, class_weight=None, criterion='gini',
            max_depth=10, max_features='auto', max_leaf_nodes=None,min_samples_leaf=1,
            min_samples_split=2, min_weight_fraction_leaf=0.0,
            n_estimators=1000, n_jobs=-1, oob_score=False, random_state=0,
            verbose=0, warm_start=False)))
		models.append(('xgboost', XGBClassifier()))
		results = []
		names = []
		for name, model in models:
			cv_results = train_test_classification(model, X, y)
			results.append(cv_results)
			names.append(name)
			msg = "%s: %f (%f)" % (name, cv_results.mean(), cv_results.std())
			print(msg)


def preparefile(filename):

	global path
	path = filename.split('/')[0]
	df = pd.read_csv(filename)

	X = df.iloc[:,0:-1]
	y = df.iloc[:,-1]

	run_classifiers(X,y)
	#run_ten_fold_classifiers(X,y)
	#random_forest_feature_selection(X,y)


