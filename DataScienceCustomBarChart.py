import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

## Load Data
np.random.seed(12345)
df = pd.DataFrame([np.random.normal(32000,200000,3650), 
                   np.random.normal(43000,100000,3650), 
                   np.random.normal(43500,140000,3650), 
                   np.random.normal(48000,70000,3650)], 
                  index=[1992,1993,1994,1995])
df_index = df.index
row_averages = df.mean(axis=1)

## Create plot
plt.bar(df_index, row_averages)
plt.xlabel('Years')
plt.xticks([1992,1993,1994,1995])
plt.ylabel('Values')
plt.show()
