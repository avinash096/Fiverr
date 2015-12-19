import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import itemfreq

data = np.genfromtxt('LIWC2007 Results1.csv', dtype=None, delimiter='\t', names=True)
for column_name in data.dtype.names[2:]:
    tmp = itemfreq(data[column_name])
    x = tmp[:, 0] # unique values in data
    y = tmp[:, 1] # frequency
    plt.loglog(x, y, basex=10, basey=10, marker='.', linestyle='None')
    plt.title(column_name)
    plt.xlabel('values')
    plt.ylabel('frequency')
    print 'Plotting for', column_name, ':', data[column_name]
    print 'x:', x
    print 'y:', y
    print
    plt.savefig(column_name+'.png', format='png')
    plt.close()
