import csv
import logging

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

class feature_file(object):

	def __init__(self,filename,featurelist):
		self.filename=filename
		self.featurelist=featurelist


	"""
	This function generates feature file to be used with sklearn or weka for machine learning. 
	"""
	def generateFeatureFile(self):
		filename,featurelist=self.filename,self.featurelist

		keys = featurelist.keys()
		with open(filename, "w", newline='') as outfile:
			writer = csv.writer(outfile, delimiter = ",")
			writer.writerow(keys)
			writer.writerows(zip(*[featurelist[key] for key in keys]))

		logger.info(" distance_between_adds_in_different_pages CSV FILE GENERATED!!!")