from collections import defaultdict
class key_val(object):

	def __init__(self):
		self.keys_list = []
		self.values_list = []
		self.add_begin_pos_dict = {}
		self.add_begin_pos_val = 0

	def set_keys_val_list(self,add_key,values):
		
		key = add_key
		self.keys_list.append(key)
		self.values_list.append(values)

		self.add_begin_pos_val=values

		if key not in self.add_begin_pos_dict:
			self.add_begin_pos_dict[key] = self.add_begin_pos_val #Stores the starting offset of each address
	
	def get_keys_list(self):
		return self.keys_list

	def get_val_list(self):
		return self.values_list

	def get_add_begin_pos_dict(self):
		return self.add_begin_pos_dict



