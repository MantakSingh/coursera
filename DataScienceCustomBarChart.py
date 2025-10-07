import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from matplotlib.cm import ScalarMappable
from matplotlib.colors import Normalize

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

# Information about the dataframe
row_averages = df.mean(axis=1) # Averages
sem_df = df.sem(axis=1)  # Standard Error of Mean
z = (row_averages - user_y_input) / sem_df  # how many SEMs away

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

max_z = 3
cmap = plt.cm.seismic  # Blue/White/Red
norm = Normalize(vmin=-max_z, vmax=max_z)
bar_colors = cmap(norm(z))

sm = ScalarMappable(cmap=cmap, norm=norm)
sm.set_array([])  # required for colorbar

##############
    # Plot
##############

plt.bar(
    row_averages.index,
    row_averages,
    color = bar_colors,
    yerr=sem_df,
    capsize=5,
    ecolor='black'
)

plt.axhline(
    y=user_y_input,
    color='black',
    linestyle='--',
    label=f'Desired y-value = {user_y_input}'
)


plt.title("Bar Chart")
plt.colorbar(sm, label='Distance from user line (in SEMs)', orientation='horizontal')
plt.xlabel('Years')
plt.xticks([1992,1993,1994,1995])
plt.ylabel('Values')
plt.legend()
plt.show()


## Click-Based
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from matplotlib.cm import ScalarMappable
from matplotlib.colors import Normalize

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

# Information about the dataframe
row_averages = df.mean(axis=1) # Averages
sem_df = df.sem(axis=1)  # Standard Error of Mean
##z = (row_averages - user_y_input) / sem_df  # how many SEMs away

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

max_z = 3
cmap = plt.cm.seismic  # Blue/White/Red
norm = Normalize(vmin=-max_z, vmax=max_z)
bar_colors = cmap(norm(z))

sm = ScalarMappable(cmap=cmap, norm=norm)
sm.set_array([])  # required for colorbar

##############
    # Plot
##############

fig, ax = plt.subplots()
bars = ax.bar(
    row_averages.index,
    row_averages,
    color=cmap(norm(np.zeros_like(row_averages))),
    yerr=sem_df,
    capsize=5,
    ecolor='black'
)

plt.axhline(
    y=user_y_input,
    color='black',
    linestyle='--',
    label=f'Desired y-value = {user_y_input}'
)

hline = ax.axhline(y=0, color='black', linestyle='--', label='Desired y-value')
plt.title("Bar Chart")
plt.colorbar(sm, label='Distance from user line (in SEMs)', orientation='horizontal')
plt.xlabel('Years')
plt.xticks([1992,1993,1994,1995])
plt.ylabel('Values')
plt.legend()

def on_click(event):
    # Check if click is inside the axes and near the y-axis (x close to 0)
    if event.inaxes == ax:
        global user_y_input
        user_y_input = event.ydata
        print(f"User clicked y-value: {user_y_input}")

        # Update horizontal line
        hline.set_ydata(user_y_input)

        # Update colors based on new y-value
        z = (row_averages - user_y_input) / sem_df
        for bar, color in zip(bars, cmap(norm(z))):
            bar.set_color(color)

        fig.canvas.draw_idle()

# Connect the click event
fig.canvas.mpl_connect('button_press_event', on_click)

plt.show()
