class feature_dictionary(object):

	def __init__(self,add_value_dict):
		self.add_value_dict=add_value_dict


	'''
	This function returns the naive features
	'''
	def get_feature_dictionary(self):
		addresskeys = self.add_value_dict.get_address_keys()
		keyAddressCounts = self.get_feature_per_key()
		logger.info("generating feature list")
		featurelist = defaultdict(list)
		
		for keypressed in keyAddressCounts:
			for key in addresskeys:
				if key in keyAddressCounts[keypressed]:
					featurelist[key].append(keyAddressCounts[keypressed][key])
				else:
					featurelist[key].append(0)
			print('neupane',keypressed.split('_')[0])
			featurelist['class'].append(charName(keypressed.split('_')[0]))

		#print featurelist['0x1f37']
		logger.debug("featurelist length %d",len(featurelist))

		return featurelist