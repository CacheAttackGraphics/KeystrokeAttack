import numpy as np
import pandas as pd
import sys,os

from matplotlib import pyplot as plt

from feature_ranker import selected_features
from classification_engine import run_classifiers
from plot_graph import plot_address
from feature_selector import filter_feature_sd

import logging

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)


def feature_ranking():
	
	logger.debug('ranking features')

	featurepath = "../"
	feature_files_list = os.listdir(featurepath)

	folders_to_analyze=['feature_diff']

	exclude = ["SkColor.cpp,19,SkPMColor SkPreMultiplyColor(SkColor c)",
"SkMask.cpp,85,void* SkMask::getAddr(int x, int y) const",
"static int maskFormatToShift(SkMask::Format format)",
"SkDraw.cpp,60,const SkPaint& paint, bool drawCoverage = false)",
"SkFontHost_FreeType_common.cpp,36,static FT_Pixel_Mode compute_pixel_mode(SkMask::Format format)",
"SkRasterClip.cpp,412,SkAAClipBlitterWrapper::SkAAClipBlitterWrapper()",
"SkFontHost_FreeType_common.cpp,36,static FT_Pixel_Mode compute_pixel_mode(SkMask::Format format)"]
	for feature_folder in feature_files_list:
		if feature_folder in folders_to_analyze:
			feature_file_list = os.listdir(featurepath+feature_folder)
			for sel_feature_file in feature_file_list:
				filter_feature_sd(featurepath+feature_folder+"/"+sel_feature_file)


	feature_file_path = "../feature_filtered/"
	feature_files = os.listdir(feature_file_path)

	for feature_file in feature_files:
		logger.debug('ranking features:%s', feature_file)
		raw_data = feature_file_path+feature_file	
		df = pd.read_csv(raw_data)
		#print(df.head())
		#for x in exclude:
		#	cols = [c for c in df.columns if x in c ]
		#	print(cols)
		#	print("*******************************************************************************************")
		#	df.drop(cols,inplace=True,axis=1)

		data_X = df.iloc[:,0:df.shape[1]-1]
		target_y = df.iloc[:,df.shape[1]-1]
		pf,data_X, selected_columns=selected_features(data_X,target_y)

		logger.debug('Ranked Features:%s',','.join(selected_columns))


		if not os.path.exists('../results/'):
		    os.makedirs('../results/')
		pf.to_csv('../results/selected_'+feature_file.split('/')[-1]+'.csv',index=False)

		run_classifiers(data_X,target_y)
		#plot_address('../results/selected_'+feature_file.split('/')[-1]+'.csv')

#feature_ranking()
