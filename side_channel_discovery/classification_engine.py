from collections import defaultdict
import numpy as np
import pandas as pd
import sys,os
import re

#model selection
from sklearn.model_selection import cross_val_score, cross_val_predict,KFold
from sklearn import metrics
from sklearn.model_selection import train_test_split
from sklearn.model_selection import LeaveOneOut
from sklearn.metrics import classification_report
from sklearn.metrics import accuracy_score
from sklearn.metrics import confusion_matrix

#Classifiers
from sklearn.naive_bayes import GaussianNB
from sklearn.neighbors import KNeighborsClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.neural_network import MLPClassifier


def train_test_classification(model, data_X, target_y):
	train_X, test_X, train_y, test_y = train_test_split(data_X, target_y, test_size=0.33, random_state=4)
	model.fit(train_X, train_y)
	y_pred = model.predict(test_X)
	print(model,classification_report(test_y, y_pred))
	return accuracy_score(test_y, y_pred, normalize=False)


def leave_one_out_classification(model,data_X,target_y):
	
	loo = LeaveOneOut()
	accuracy_score = defaultdict(list)
	
	for train_index, test_index in loo.split(data_X):
		X_train, X_test = data_X.values[train_index], data_X.values[test_index]
		y_train, y_test = target_y.values[train_index], target_y.values[test_index]
		model.fit(X_train, y_train)
		predictions = model.score(X_test,y_test)
		accuracy_score[model].append(predictions)

	return accuracy_score

def cross_fold_validation(model, data_X, target_y,name):
	seed = 0
	#kfold = KFold(n_splits=10, random_state=seed)
	cv_report = cross_val_score(model, data_X, target_y, cv=10)
	target_y_pred = cross_val_predict(model, data_X, target_y, cv=10)
	report = classification_report(target_y, target_y_pred)
	print(confusion_matrix(target_y, target_y_pred))
	classifaction_report_csv(report,name)
	return cv_report

def classifaction_report_csv(report,modeltype):
	report_data = []
	lines = report.split('\n')
	for line in lines[2:-3]:
		row_data = re.split('\s+', line.strip())
		row = {}
		row['class'] = row_data[0]
		row['precision'] = float(row_data[1])
		row['recall'] = float(row_data[2])
		row['f1_score'] = float(row_data[3])
		row['support'] = float(row_data[4])
		report_data.append(row)
	dataframe = pd.DataFrame.from_dict(report_data)
	dataframe.to_csv('../results/classification_report'+modeltype+'.csv', index = False)

#report = classification_report(y_true, y_pred)
#classifaction_report_csv(report)

def run_classifiers(data_X,target_y):
		
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