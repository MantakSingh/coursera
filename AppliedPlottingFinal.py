import pandas as pd
import numpy as np
import matplotlib.pyplot  as plt
from matplotlib.backends.backend_tkagg import (
     FigureCanvasTkAgg, NavigationToolbar2Tk)
from tkinter import *
from tkinter import ttk
'''
This program plots the correlation between rates of female homicide and rates of contraceptive usage. My hypothesis is that as contraceptive use increases,
female homicide rates decrease. The idea being that higher contraceptive usage indicates societies that value women more highly. 
'''

##############
 ## Load Data
##############

## Homicide Dataframe

# Load Female homicide data
female_homicide_df = pd.read_excel(r"C:\Users\kensi\Downloads\Intentional homicide victims by sex, counts and ra.xls", skiprows = 1)
female_homicide_cleaned_df = female_homicide_df[female_homicide_df['Sex'] == 'Female']

# Need Percentage of Homicides to do correlation with the contraception rates
female_homicide_rates_df = pd.DataFrame()
female_homicide_rates_df["Country"] = female_homicide_cleaned_df["Country"]

# Years for Homicide Percentage Dataframe
year_columns = [str(year) for year in range(2000, 2024)]

# Get the percentage of homicide rather than the rate for 100K
for year in year_columns:
    count_col = year        # deaths
    rate_col = year + '.1'  # rate per 100,000
    pop = 0 # Placeholder
    # Only calculate if both columns exist in the dataset
    if count_col in female_homicide_cleaned_df.columns and rate_col in female_homicide_cleaned_df.columns:
        # Convert rate per 100k into percentage
        pop = (female_homicide_cleaned_df[count_col] * 100000) / female_homicide_cleaned_df[rate_col] 
        female_homicide_rates_df[year] = (female_homicide_cleaned_df[count_col] / pop) * 100
    else:
        female_homicide_rates_df[year] = np.nan ## Error prevention

# Rename Countries
female_homicide_rates_df["Country"] = female_homicide_rates_df["Country"].replace({
    "United Kingdom (Scotland)": "United Kingdom",
    "United Kingdom (Northern Ireland)": "United Kingdom",
    "United Kingdom (England and Wales)": "United Kingdom",
    "Netherlands (Kingdom of the)": "Netherlands",
    "Türkiye": "Turkey"
})

# Merge the United Kingdom rows together
female_homicide_rates_df = female_homicide_rates_df.groupby("Country", as_index=False).sum()

# Create new row for the means of each year
mean_row = female_homicide_rates_df.mean(numeric_only=True)
mean_row.name = 'Mean'
female_homicide_rates_df = pd.concat([female_homicide_rates_df, pd.DataFrame([mean_row])], ignore_index=False)

## Contraceptive Dataframe

# Load the Contraceptive Dataframe 
contraceptive_prevalence_df = pd.read_excel(r"C:\Users\kensi\Downloads\Contraceptive Prevalence Method.xls", skiprows = 3)
contraceptive_prevalence_df = contraceptive_prevalence_df[["Country", "Year(s)", "Any method"]]
contraceptive_prevalence_df.rename(columns={'Any method': 'Contraceptive Use Percentage'}, inplace=True)

# Break up the hyphenated year ranges into multiple rows
def expand_year_ranges(df):
    expanded_rows = []

    for _, row in df.iterrows():
        year_value = row["Year(s)"]

        # Skip rows where Year(s) is NaN or not usable
        if pd.isna(year_value):
            continue

        year_str = str(year_value).strip()

        # Handle year ranges like "1972-1974"
        if "-" in year_str:
            try:
                start, end = map(int, year_str.split("-"))
                for y in range(start, end + 1):
                    new_row = row.copy()
                    new_row["Year(s)"] = y
                    expanded_rows.append(new_row)
            except ValueError:
                # Skip malformed ranges (e.g., "201a-201b")
                continue

        # Handle single years (even if stored as strings)
        else:
            try:
                y = int(float(year_str))
                new_row = row.copy()
                new_row["Year(s)"] = y
                expanded_rows.append(new_row)
            except ValueError:
                continue

    expanded_df = pd.DataFrame(expanded_rows)
    return expanded_df.reset_index(drop=True)
    
# Apply the previous function
contraceptive_prevalence_df = expand_year_ranges(contraceptive_prevalence_df)

# Convert columns to numeric safely
contraceptive_prevalence_df["Year(s)"] = pd.to_numeric(contraceptive_prevalence_df["Year(s)"], errors="coerce")
contraceptive_prevalence_df["Contraceptive Use Percentage"] = pd.to_numeric(contraceptive_prevalence_df["Contraceptive Use Percentage"], errors="coerce")
contraceptive_prevalence_df = contraceptive_prevalence_df.replace([np.inf, -np.inf], np.nan).dropna(subset=["Year(s)", "Contraceptive Use Percentage"])

# Rename countries
contraceptive_prevalence_df["Country"].replace({
    'China, Hong Kong SAR': 'Hong Kong',
    'The former Yugoslav Republic of Macedonia': 'North Macedonia'
}, inplace=True
)

# Global Mean column
contraceptive_prevalence_df['Mean Contraceptive Use (%)'] = (
    contraceptive_prevalence_df.groupby('Year(s)')['Contraceptive Use Percentage']
      .transform('mean')
)

######################
  # Global Variables
######################

# Global merged dataframe that displays the global means for each year
merged_df = pd.DataFrame(columns=female_homicide_rates_df.columns)
merged_df.drop('Country', axis = 'columns', inplace=True)
merged_df.loc['Female Homicide Percentage Mean'] = female_homicide_rates_df.loc['Mean']

# Flip the columns to the index
merged_series = merged_df.loc['Female Homicide Percentage Mean'] # This is only temporary / I'm not using this again
merged_df = merged_series.reset_index() # Make it into a dataframe
merged_df.set_index('index', inplace= True) # Make the column an index
merged_df.index = merged_df.index.astype(int) # Fix the type
yearly_mean_series = (
    contraceptive_prevalence_df.groupby('Year(s)')['Contraceptive Use Percentage']
      .mean()
)

yearly_mean_df = yearly_mean_series.reset_index() 
yearly_mean_df.set_index('Year(s)',inplace= True)

merged_df = merged_df.join(yearly_mean_df)
merged_df = merged_df.dropna()

def show_plot(selected_country: str):
    global ax, canvas  # Load the existing plot
    ax.clear()  # Clear previous graphs

    # Filter dataframes by desired country
    selected_contraceptive_df = contraceptive_prevalence_df[
        contraceptive_prevalence_df['Country'] == selected_country
    ]
    selected_homicide_df = female_homicide_rates_df[
        female_homicide_rates_df["Country"] == selected_country
    ]
    
    # If no data found in either dataframe
    if selected_contraceptive_df.empty or selected_homicide_df.empty:
        ax.text(
            0.5, 0.5,
            f"Insufficient data for {selected_country}",
            ha='center', va='center',
            fontsize=14, color='red', style='italic'
        )
        ax.set_title(f"{selected_country}: Insufficient Data")
        canvas.draw()
        return

    # Clean contraceptive dataframe
    selected_contraceptive_df = selected_contraceptive_df.drop(
        ["Mean Contraceptive Use (%)", "Country"], axis=1
    ).T
    selected_contraceptive_df.columns = selected_contraceptive_df.loc['Year(s)']
    selected_contraceptive_df = selected_contraceptive_df.drop("Year(s)")
    selected_contraceptive_df.columns = selected_contraceptive_df.columns.astype(int)
    selected_contraceptive_df = selected_contraceptive_df.T

    # Clean homicide dataframe
    selected_homicide_df = selected_homicide_df.T
    selected_homicide_df.columns = selected_homicide_df.iloc[0]
    selected_homicide_df = selected_homicide_df.drop("Country")
    selected_homicide_df.columns = ['Female Homicide Percentage Mean']
    selected_homicide_df.index = selected_homicide_df.index.astype(int)
    
    # Merge data
    desired_df = pd.merge(
        selected_homicide_df, selected_contraceptive_df,
        left_index=True, right_index=True
    )
    plot_df = desired_df.apply(pd.to_numeric, errors='coerce').dropna(
        subset=["Contraceptive Use Percentage", "Female Homicide Percentage Mean"]
    )

    # Check for insufficient data
    if plot_df.shape[0] < 2:
        ax.text(
            0.5, 0.5,
            f"Insufficient data for {selected_country}",
            ha='center', va='center',
            fontsize=14, color='red', style='italic'
        )
        ax.set_title(f"{selected_country}: Insufficient Data")
        canvas.draw()
        return

    x = plot_df["Contraceptive Use Percentage"].values
    y = plot_df["Female Homicide Percentage Mean"].values

    try:
        m, b = np.polyfit(x, y, 1)
        corr = np.corrcoef(x, y)[0, 1]
        if np.isnan(corr) or np.isnan(m):
            raise ValueError("Invalid trendline or correlation")
    except Exception:
        ax.text(
            0.5, 0.5,
            f"Insufficient data for {selected_country}",
            ha='center', va='center',
            fontsize=14, color='red', style='italic'
        )
        ax.set_title(f"{selected_country}: Insufficient Data")
        canvas.draw()
        return

    # Plot valid data
    ax.scatter(x, y, alpha=0.7, color='blue', label='Data points')
    ax.plot(x, m*x + b, color='red', linewidth=2, label=f'Trendline (r={corr:.2f})')
    ax.set_xlabel("Contraceptive Use Percentage")
    ax.set_ylabel("Female Homicide Percentage Mean")
    ax.set_title(f"{selected_country}: Female Homicide vs Contraceptive Use")
    ax.legend()
    ax.grid(True, linestyle='--', alpha=0.5)

    # Redraw Tkinter canvas
    canvas.draw()

def button_command():
    selected = listbox.curselection()
    if selected:
        country = listbox.get(selected[0])
        show_plot(country)

####################
  # User Interface
####################

# Initialize Tkinter
root = Tk()
root.title("Correlation Program")

fig, ax = plt.subplots()
canvas = FigureCanvasTkAgg(fig, master=root)  
canvas.get_tk_widget().pack(side=TOP, fill=BOTH, expand=1)

# Label
label = Label(root, text="Select a Country", font=("Courier", 24))
label.pack(pady=10)

# Create Combobox with country list
countries = sorted(female_homicide_rates_df["Country"].dropna().unique())

country_combobox = ttk.Combobox(
    root,
    values=countries,
    state="readonly",   # Only allow selection (no free typing)
    width=40,
    font=("Helvetica", 12)
)
country_combobox.pack(pady=5)

# Default selection prompt
country_combobox.set("Select a country")

# Event handler for Combobox selection
def on_country_selected(event):
    selected_country = country_combobox.get()
    if selected_country in countries:
        show_plot(selected_country)
    else:
        ax.clear()
        ax.text(
            0.5, 0.5,
            "Please select a valid country",
            ha="center", va="center", fontsize=14
        )
        canvas.draw()

# Bind event to combobox selection
country_combobox.bind("<<ComboboxSelected>>", on_country_selected)

root.mainloop()
