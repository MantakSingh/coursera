import pandas as pd
import numpy as np
import matplotlib.pyplot  as plt
import re
'''
# Set options to display all rows and columns
pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns', None)
pd.set_option('display.width', None) # Adjust for wider output
pd.set_option('display.max_colwidth', None) # Display full content of cells
'''
'''
This program plots the correlation between rates of female homicide and rates of contraceptive usage. My hypothesis is that as contraceptive use increases,
female homicide rates decrease. The idea being that higher contraceptive usage indicates societies that value women more highly. 
'''
##############
 ## Load Data
##############

# Load Female homicide data
female_homicide_df = pd.read_excel(r"C:\Users\kensi\Downloads\Intentional homicide victims by sex, counts and ra.xls", skiprows = 1)
female_homicide_cleaned_df = female_homicide_df[female_homicide_df['Sex'] == 'Female']

# Need Percentage of Homicides to do correlation with the contraception rates
female_homicide_rates_df = pd.DataFrame()
female_homicide_rates_df["Country"] = female_homicide_cleaned_df["Country"]

# Years for Homicide Percentage
year_columns = [str(year) for year in range(2000, 2024)]

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

female_homicide_rates_df["Country"] = female_homicide_rates_df["Country"].replace({
    "United Kingdom (Scotland)": "United Kingdom",
    "United Kingdom (Northern Ireland)": "United Kingdom",
    "United Kingdom (England and Wales)": "United Kingdom",
    "Netherlands (Kingdom of the)": "Netherlands",
    "Türkiye": "Turkey"
})

# Aggregate
female_homicide_rates_df = female_homicide_rates_df.groupby("Country", as_index=False).sum()

# Create new row for the means of each year
mean_row = female_homicide_rates_df.mean(numeric_only=True)
mean_row.name = 'Mean'
female_homicide_rates_df = pd.concat([female_homicide_rates_df, pd.DataFrame([mean_row])], ignore_index=False)

# Load Contraceptive data
contraceptive_prevalence_df = pd.read_excel(r"C:\Users\kensi\Downloads\Contraceptive Prevalence Method.xls", skiprows = 3)
contraceptive_prevalence_df = contraceptive_prevalence_df[["Country", "Year(s)", "Any method"]]
contraceptive_prevalence_df.rename(columns={'Any method': 'Contraceptive Use Percentage'}, inplace=True)

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
    
contraceptive_prevalence_df = expand_year_ranges(contraceptive_prevalence_df)

# Convert columns to numeric safely
contraceptive_prevalence_df["Year(s)"] = pd.to_numeric(contraceptive_prevalence_df["Year(s)"], errors="coerce")
contraceptive_prevalence_df["Contraceptive Use Percentage"] = pd.to_numeric(contraceptive_prevalence_df["Contraceptive Use Percentage"], errors="coerce")

contraceptive_prevalence_df = contraceptive_prevalence_df.replace([np.inf, -np.inf], np.nan).dropna(subset=["Year(s)", "Contraceptive Use Percentage"])

contraceptive_prevalence_df["Country"].replace({
    'China, Hong Kong SAR': 'Hong Kong',
    'The former Yugoslav Republic of Macedonia': 'North Macedonia'
}, inplace=True
)

contraceptive_prevalence_df['Mean Contraceptive Use (%)'] = (
    contraceptive_prevalence_df.groupby('Year(s)')['Contraceptive Use Percentage']
      .transform('mean')
)

## Global variables

# Global merged dataframe
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
    
# Turn the countries of each Dataframe into a series
homicide_countries = female_homicide_rates_df["Country"]
contraceptive_countries = contraceptive_prevalence_df["Country"]

# Group repeating countries into single entries
contraceptive_countries = contraceptive_countries.unique()
contraceptive_countries = pd.Series(contraceptive_countries) # Turn NumPy Array back into a Pandas Series
contraceptive_countries.name = 'Country'
contraceptive_countries = contraceptive_countries.dropna()

homicide_countries = homicide_countries.shift(-1)
homicide_countries.drop(index = [157, 'Mean'], inplace= True)

homicide_countries = homicide_countries.dropna()

missing_in_contraceptive = set(homicide_countries.dropna()) - set(contraceptive_countries.dropna())
missing_in_homicide = set(contraceptive_countries.dropna()) - set(homicide_countries.dropna())

missing_countries = []
for value in homicide_countries:
    if value not in contraceptive_countries.values:
        missing_countries.append(value)

def show_plot(selected_country: str):

    ## Create shared dataframe

    # Filter dataframes by desired country
    selected_contraceptive_df = contraceptive_prevalence_df[contraceptive_prevalence_df['Country']==selected_country]
    selected_homicide_df = female_homicide_rates_df[female_homicide_rates_df["Country"]==selected_country]
    
    # Clean contraceptive dataframe
    selected_contraceptive_df.drop(["Mean Contraceptive Use (%)", "Country"], axis = 1, inplace= True) # Drop Global mean & Country column
    selected_contraceptive_df = selected_contraceptive_df.T # Flip the Dataframe
    selected_contraceptive_df.columns = selected_contraceptive_df.loc['Year(s)']
    selected_contraceptive_df.drop(index = "Year(s)", inplace= True)
    selected_contraceptive_df.columns = selected_contraceptive_df.columns.astype(int) # Fix the type
    selected_contraceptive_df = selected_contraceptive_df.T

    # Clean homicide dataframe
    selected_homicide_df = selected_homicide_df.T
    selected_homicide_df.columns = selected_homicide_df.iloc[0]
    selected_homicide_df.drop("Country", axis = 0, inplace = True)
    selected_homicide_df.columns = ['Female Homicide Percentage Mean']
    selected_homicide_df.index.name = 'Year(s)'
    selected_homicide_df.index = selected_homicide_df.index.astype(int) # Fix Index data type

    # Create the new merged dataframe
    desired_df = pd.merge( selected_homicide_df, selected_contraceptive_df, left_index=True, right_index=True)

    ## Plot

    # Make a copy to be safe
    plot_df = desired_df.copy()

    # Ensure numeric values and dropping invalid rows
    plot_df = plot_df.apply(pd.to_numeric, errors='coerce').dropna(subset=["Contraceptive Use Percentage", "Female Homicide Percentage Mean"])

    # Extract x and y as floats
    x = plot_df["Contraceptive Use Percentage"].values
    y = plot_df["Female Homicide Percentage Mean"].values

    # Fit linear trendline
    m, b = np.polyfit(x, y, 1)

    # Compute correlation
    #corr = np.corrcoef(x, y)[0,1]
    corr = plot_df.corr()
    return corr
    '''
    # Plot
    plt.figure(figsize=(8,6))
    plt.scatter(x, y, alpha=0.7, color='blue', label='Data points')
    plt.plot(x, m*x + b, color='red', linewidth=2, label=f'Trendline (r={corr:.3f})')
    plt.xlabel("Contraceptive Use Percentage")
    plt.ylabel("Female Homicide Percentage Mean")
    plt.title(f"Correlation: Female Homicide Rate vs Contraceptive Use for {selected_country}")
    plt.legend()
    plt.grid(True, linestyle='--', alpha=0.5)
    plt.show()
    '''

show_plot('United Kingdom')
