import numpy as np
import matplotlib.pyplot as plt
from matplotlib import cm
import pandas as pd
import seaborn as sn

conf_arr = [[16,0,0,0,0,0,0,0,0,0], 
[0,14,0,1,1,0,0,2,0,0], 
[0,0,10,0,0,0,4,0,0,1], 
[0,4,0,9,1,0,4,1,0,0], 
[0,1,0,0,11,3,0,1,0,1], 
[0,0,0,0,1,13,0,0,0,1],
[0,1,1,0,4,0,11,0,0,0], 
[2,1,0,1,3,0,0,9,0,1], 
[0,0,0,0,0,0,0,0,17,0],
[0,1,0,0,3,1,0,0,0,14]]

def use_imshow():
    norm_conf = []
    for i in conf_arr:
        a = 0
        tmp_arr = []
        a = sum(i, 0)
        for j in i:
            tmp_arr.append(float(j)/float(a))
        norm_conf.append(tmp_arr)

    fig = plt.figure()
    plt.clf()
    ax = fig.add_subplot(111)
    ax.set_aspect(1)
    res = ax.imshow(np.array(norm_conf), cmap=cm.jet, #coolwarm 
                    interpolation='nearest')

    width, height = np.array(conf_arr).shape

    #for x in range(width):
    #    for y in range(height):
    #        ax.annotate(str(round(norm_conf[x][y],2)), xy=(y, x), 
    #                    horizontalalignment='center',
    #                    verticalalignment='center')

    cb = fig.colorbar(res)
    alphabet = '0123456789'
    plt.xticks(range(width), alphabet[:width])
    plt.yticks(range(height), alphabet[:height])
    plt.savefig('confusion_matrix_digits.png', format='png')

def use_heatmap():
    df_cm = pd.DataFrame(conf_arr, index = [i for i in "0123456789"],
                  columns = [i for i in "0123456789"])
    plt.figure(figsize = (10,7))
    sn.heatmap(df_cm, annot=True)
    plt.show()

use_imshow()