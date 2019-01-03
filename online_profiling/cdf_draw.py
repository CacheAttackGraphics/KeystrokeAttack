import pandas as pd
from matplotlib import pyplot as plt

def plotCdf(data, labels, outfile="out.png"):
	fig, ax = plt.subplots()
	plt.xlabel("Number of guesses");
	plt.ylabel("CDF");
	#plt.xlim(-3000,3000);
	ax.set_ylim(0, 1.05);
	ax.set_xlim(1, 100000000000000);
	for i in range(len(data)):
		results = list(map(float, data[i]))
		x = sorted(results);
		#for j in range(len(x)):
			#print(x[j]);
		#exit(0)
		y = [float(j) / len(data[i]) for j in range(len(data[i]))];
		ax.semilogx(x, y, label=labels[i]);
	ax.grid()
	ax.legend(loc=0);
	plt.savefig(outfile);
	plt.show();

df1 = pd.read_csv("results_modeled_with_confidence_avg_one.csv",header=None,names=["pwd","modeled"])
mod_avg_one = df1["modeled"].values


df2 = pd.read_csv("results_random.csv",header=None,names=["pwd","random"])
rand_base = df2["random"].values


df4 = pd.read_csv("results_modeled_with_confidence_avg.csv",header=None,names=["pwd","modeled"])
mod_avg_ten= df4["modeled"].values

plotCdf([rand_base, mod_avg_one, mod_avg_ten], ["Random", "mod_avg_one","mod_avg_ten"], outfile="out.png")

