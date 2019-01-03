import pandas as pd
import numpy as np
import os
import sys
from matplotlib import pyplot as plt


def plot_address(file_to_plot):
	df = pd.read_csv(file_to_plot)
	#df =df.drop(df.columns[0],axis=1)
	print("plot address",list(df.columns.values))
	fig, ax = plt.subplots()
	df.plot(x='class',y=list(df.loc[:, df.columns != 'class'].columns.values),ax=ax,kind='line',title=file_to_plot,grid=True,legend=True)
	start, end = ax.get_ylim()
	interval = 4000 if start > 1000 else 10
	#fig.suptitle('test title', fontsize=20)
	plt.xlabel('digits', fontsize=12)
	plt.ylabel('no_of_inst', fontsize=9)
	ax.yaxis.set_tick_params(labelsize=6)
	ax.yaxis.set_ticks(np.arange(0, end, interval))
	ax.xaxis.set_ticks(np.arange(len(df['class'].values)))
	ax.set_xticklabels(df['class'].values)
	ax.xaxis.set_tick_params(labelsize=6)
	plt.xticks(rotation=70)
	if not os.path.exists('../results/'):
	    os.makedirs('../results/')
	plt.savefig('../results/'+file_to_plot+'.pdf')
	#plt.show()
