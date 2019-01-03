class key_generator(object):

	def __init__(self,filename):
		self.filename= filename

	def get_key(self):
		key_name = self.filename.split('/')[-1]
		print(str(key_name).split('.',1)[0])
		return str(key_name).split('.',1)[0]