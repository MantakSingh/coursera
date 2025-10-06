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

# Setting horizontal line based on user input
user_y_input = input("What y-value do you want?")
user_y_input = float(user_y_input)
plt.axhline(y = user_y_input, color='b', linestyle='--', label='Horizontal Line at y=0.5')

# Determining bar's relative position to line
def cv(value):
    if value == user_y_input:
        return 'yellow'
    elif value > user_y_input:
        return 'red'
    else:
        return 'blue'
    
# Setting Colors
bar_labels = ['1992', '1993', '1994', '1995']
bar_colors = [cv(row_averages.loc[1992]), cv(row_averages.loc[1993]), cv(row_averages.loc[1994]), cv(row_averages.loc[1995])]

# Generating bar chart
plt.bar(df_index, row_averages, label=bar_labels, color=bar_colors)
plt.title("Bar Chart")
plt.xlabel('Years')
plt.xticks([1992,1993,1994,1995])
plt.ylabel('Values')
plt.show()
