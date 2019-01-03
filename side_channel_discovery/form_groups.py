from collections import defaultdict
import csv

class form_groups(object):

	def __init__(self,key_val):
		self.pagedict=key_val.get_page_dict()
		self.keys=key_val.get_keys_list()
		self.add_pos_group = defaultdict(list)
		self.min_page_group = defaultdict(list)

	def get_groups_after_prefetch_check(self):

		#output = open('log_writer.txt','a')
	
		for dictkey in self.pagedict:
		#print('**creating group for dict**',dictkey)
			#splitting the add pairs for each library
			all_library_data = defaultdict(set)
			data_keys = self.pagedict[dictkey]	

			for each_key in data_keys:
				key_id,lib = each_key.split('_')[0], '_'.join(each_key.split('_')[1:])
				all_library_data[lib].add(int(key_id,0))
				
			#end of the split logic

			groups = defaultdict(set)
			groupid = 0


			for lib_key in all_library_data:
				data = all_library_data[lib_key]
				start = sorted(data)[0]
				#make groups of addresses
				for item in sorted(data):
					item_key = hex(item) + '_' + lib_key
					if item- start < 8:
						groups[groupid].add(item_key)
					else:
						groupid+=1
						groups[groupid].add(item_key)
					start=item

			
			# output.write('************Start**************\n\n\n')
			
			# for grpkey in groups:
			# 	output.write(str(grpkey) +","+ ','.join(groups[grpkey]) +"\n")
			# output.write('************End**************\n\n\n')
			

			# output.write("*************start of the minimum occurence list*****************")

			#find minimum/first appearing address in the group
			for grpkey in groups:
				all_occ = []
				
				#find all occurrences of an address in the list of keys
				for item in groups[grpkey]:
					all_occ += [index for index, value in enumerate(self.keys) if value == item] 
				
				for all_item in all_occ:
					self.add_pos_group[dictkey+"_"+str(grpkey)].append(all_item)
				
				self.min_page_group[dictkey].append((self.keys[min(all_occ)],grpkey)) #append the first appearing address of the group, and the group id
				#output.write(str(grpkey)+","+self.keys[min(all_occ)]+"\n")
			
			#output.write("*************end of the minimum occurence list*****************")
		return self.add_pos_group,self.min_page_group
