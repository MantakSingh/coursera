import matplotlib.pyplot as plt
from calendar import month_abbr
import numpy as np

######################
    # Import Data
######################

# Import main df
df = pd.read_csv('assets/fb441e62df2d58994928907a91895ec62c2c42e6cd075c2700843b89.csv')

# Cleaning main dataframe
df['Date'] = pd.to_datetime(df['Date'])
df["Data_Value"] = df["Data_Value"].apply(lambda x: x/10)

# Creating Max/Min dataframes
TMAX_df = df[df['Element'] == 'TMAX']
TMIN_df = df[df['Element'] == 'TMIN']

######################
    # Decade Data
######################

# Create a DataFrame of maximum temperature by date
tmax_decade = TMAX_df[(TMAX_df['Date'].dt.year >= 2005) & (TMAX_df['Date'].dt.year <= 2014)]
tmax_decade = tmax_decade[tmax_decade['Date'].dt.strftime('%m-%d') != '02-29']
tmax_grouped = tmax_decade.groupby('Date')['Data_Value'].mean().reset_index()

# Create a DataFrame of minimum temperatures by date
tmin_decade = TMIN_df[(TMIN_df['Date'].dt.year >= 2005) & (TMIN_df['Date'].dt.year <= 2014)]
tmin_decade = tmin_decade[tmin_decade['Date'].dt.strftime('%m-%d') != '02-29']
tmin_grouped = tmin_decade.groupby('Date')['Data_Value'].mean().reset_index()

# Create a month-day column for grouping
tmax_grouped['month_day'] = tmax_grouped['Date'].dt.strftime('%m-%d')
tmin_grouped['month_day'] = tmin_grouped['Date'].dt.strftime('%m-%d')

tmax_decade_max = tmax_grouped.groupby('month_day')['Data_Value'].max().reset_index()
tmin_decade_min = tmin_grouped.groupby('month_day')['Data_Value'].min().reset_index()

######################
     # 2015 Data
######################

# Calculate the minimum and maximum values for the year 2015
tmax_2015 = TMAX_df[TMAX_df['Date'].dt.year == 2015]
tmin_2015 = TMIN_df[TMIN_df['Date'].dt.year == 2015]

# Remove Feb 29
tmax_2015 = tmax_2015[tmax_2015['Date'].dt.strftime('%m-%d') != '02-29']
tmin_2015 = tmin_2015[tmin_2015['Date'].dt.strftime('%m-%d') != '02-29']

# Create a month-day column for grouping
tmax_2015['month_day'] = tmax_2015['Date'].dt.strftime('%m-%d')
tmin_2015['month_day'] = tmin_2015['Date'].dt.strftime('%m-%d')

tmax_2015_daily = tmax_2015.groupby('month_day')['Data_Value'].mean().reset_index()
tmin_2015_daily = tmin_2015.groupby('month_day')['Data_Value'].mean().reset_index()


######################
        # Plot        
######################

# Plot Basics
plt.figure(figsize=(10,6))
plt.figure(figsize=(12,6), facecolor='white')  # Prevents Transparency

# Plot historical min/max as lines
plt.plot(tmax_decade_max['month_day'], tmax_decade_max['Data_Value'], '-', color='orange', label='2005-2014 Max')
plt.plot(tmin_decade_min['month_day'], tmin_decade_min['Data_Value'], '-', color='skyblue', label='2005-2014 Min')

# Shading
plt.fill_between(
    tmax_decade_max['month_day'],
    tmin_decade_min['Data_Value'],
    tmax_decade_max['Data_Value'],  
    color='white',    # base fill color
    hatch='/',        # diagonal lines
    edgecolor='lightgray', 
    linewidth=0.5     
)

# Identify record-breaking 2015 temps
tmax_breaks = tmax_2015_daily[tmax_2015_daily['Data_Value'] > tmax_decade_max['Data_Value']]
tmin_breaks = tmin_2015_daily[tmin_2015_daily['Data_Value'] < tmin_decade_min['Data_Value']]

# Scatter plot for record-breaking days
plt.scatter(tmax_breaks['month_day'], tmax_breaks['Data_Value'], s=10, color='red', label='2015 Record Highs')
plt.scatter(tmin_breaks['month_day'], tmin_breaks['Data_Value'], s=10, color='blue', label='2015 Record Lows')

# Set x-axis ticks to the first day of each month
months = pd.date_range('2000-01-01', '2000-12-31', freq='MS')  # just need month start dates
month_labels = [month_abbr[m.month] for m in months]
month_ticks = [m.strftime('%m-%d') for m in months]
plt.xticks(ticks=month_ticks, labels=month_labels, rotation=0)  # rotation optional

# Actual Plotting
plt.xlabel('Day of Year')
plt.ylabel('Temperature (°C)')
plt.title('Daily Temperature Records (2005–2014) vs. 2015 Temperature Records')
plt.legend()
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()
