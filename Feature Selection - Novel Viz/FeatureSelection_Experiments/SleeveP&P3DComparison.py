import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

from mpl_toolkits.mplot3d import Axes3D

DatabaseDF = pd.read_csv('Feature Selection - Novel Viz\CleanedDataset.csv')

filteredDF = DatabaseDF[DatabaseDF['Completion Type'] == 'Sleeves and P & P']

fig = plt.figure(figsize = (15,10))
ax = fig.add_subplot(111, projection = '3d')
ax.scatter(filteredDF['Sleeves'], filteredDF['P&P'], filteredDF['12 month Cum Prod'], s = 200)
ax.set(xlabel = 'Sleeves', ylabel = 'P & P', zlabel = '12 month Cum Prod')

plt.show()