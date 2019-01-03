from collections import defaultdict

class add_value(object):

	def __init__(self):
		self.feature_per_key = defaultdict(list)
		self.address_keys = set()

	def set_address_keys(self,add_key):
		self.address_keys.add(add_key)

	def get_address_keys(self):
		return self.address_keys

	'''
	key is filename, feature_dict is the feature related to each key-press file
	'''
	def set_feature_per_key(self,key,feature_dict):
		self.feature_per_key[key] = feature_dict

	def get_feature_per_key(self):
		return self.feature_per_key