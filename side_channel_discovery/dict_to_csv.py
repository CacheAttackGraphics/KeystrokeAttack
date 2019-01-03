import csv

def dict_to_csv(dics):
	print(list(dics.keys()))
	with open("../feature_count/file.csv",'w') as out_file:
	   # Using dictionary keys as fieldnames for the CSV file header
	    writer = csv.DictWriter(out_file, fieldnames=list(dics.keys()), dialect='excel')
	    writer.writeheader()
	    writer.writerows(dics)