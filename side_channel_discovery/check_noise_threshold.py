from collections import Counter

class check_noise_threshold(object):
	def __init__(self,key1,key2,keys,vals):
		self.keys = keys
		self.vals=vals
		self.key1 = key1
		self.key2 = key2
		self.count_dict=Counter(keys)

	def find_distances(self,grp1,grp2):
		#output = open('../results/program_trace_log.txt','a')
		fafa = min(grp1) #first address first appearance
		safa = min(grp2) #second address first appearance
		#print("**********************************",grp1)
		fala = max(grp1) #first address last appearance

		if fala < safa: 
			a = [safa-x for x in grp1] #this is a temporary array with indexes 
			closest_index = min([n for n in a if n>0])
			falabs=grp1[a.index(closest_index)] #if closest then the difference is minimum, so max
			#first address last appearnace before second address - # first appearance of the first address. The distance should be as low as possible
			dist_falabs = sum(self.vals[0:falabs]) #first address last appearance before second address
			if falabs == fala:
				print("going right Ajaya")
			else:
				print("Check your code: Somethign is wrong in there",fala,falabs)
			dist_fafa = sum(self.vals[0:fafa]) #distance first appearance first address
			if dist_falabs - dist_fafa > 4000: #if range of the first group is greater than 4000 instructions, then the noise will be high 
				return False
			else:
				dist_safa = sum(self.vals[0:safa]) #distance second address first appearance
				if dist_safa - dist_falabs > 10000: #if the distance between two address is less than 4000, they may not be good signal pairs.
					return True
				else:
					return False
		else:
			return False

	def get_noise_level_check(self):

		grp1 = self.groups[self.key1+"_"+str(self.grpid1)]
		grp2 = self.groups[self.key2+"_"+str(self.grpid2)]

		if min(grp1) < min(grp2):
			return self.find_distances(grp1,grp2)
		else:
			return self.find_distances(grp2,grp1)

