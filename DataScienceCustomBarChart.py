import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

##############
 # Load Data
##############

np.random.seed(12345)
df = pd.DataFrame([np.random.normal(32000,200000,3650), 
                   np.random.normal(43000,100000,3650), 
                   np.random.normal(43500,140000,3650), 
                   np.random.normal(48000,70000,3650)], 
                  index=[1992,1993,1994,1995])
df_index = df.index
row_averages = df.mean(axis=1)
std_dev_df = df.sem(axis=1)  # Standard Error of Mean(Standard Deviation is huge)

##############
 # User Input
##############

try:
    user_y_input = float(input("Enter a y-value: "))
except ValueError:
    print("Invalid input. Defaulting to 0.")
    user_y_input = 0.0
    
##############
 # Bar Color
##############

def color_for_value(value, threshold):
    "Return bar color based on comparison to threshold."
    if value > threshold:
        return 'red'
    elif value < threshold:
        return 'blue'
    return 'yellow'
    
# Setting Colors
bar_colors = [color_for_value(v, user_y_input) for v in row_averages]

##############
    # Plot
##############

plt.bar(row_averages.index, row_averages, color=bar_colors)
plt.axhline(y=user_y_input, color='black', linestyle='--', label=f'y = {user_y_input}')
plt.errorbar(row_averages.index, row_averages, yerr=std_dev_df, fmt="", color="r", capthick = 1)

plt.title("Bar Chart")
plt.xlabel('Years')
plt.xticks([1992,1993,1994,1995])
plt.ylabel('Values')
plt.legend()
plt.tight_layout()
plt.show()
