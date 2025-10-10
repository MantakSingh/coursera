import pandas as pd
import numpy as np
import matplotlib.pyplot  as plt
import re

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

# Load Contraceptive data
contraceptive_prevalence_df = pd.read_excel(r"C:\Users\kensi\Downloads\Contraceptive Prevalence Method.xls", skiprows = 3)
contraceptive_prevalence_df = contraceptive_prevalence_df[["Country", "Year(s)", "Any method"]]

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
contraceptive_prevalence_df["Any method"] = pd.to_numeric(contraceptive_prevalence_df["Any method"], errors="coerce")

contraceptive_prevalence_df = contraceptive_prevalence_df.replace([np.inf, -np.inf], np.nan).dropna(subset=["Year(s)", "Any method"])

##############
    # Plot
##############

# Ensure we have valid numeric data

x = contraceptive_prevalence_df["Year(s)"].astype(float)
y = contraceptive_prevalence_df["Any method"].astype(float)

# Fit a 1st degree polynomial (a straight line)
m, b = np.polyfit(x, y, 1)

# Plot scatter points
plt.scatter(x, y, label="Data", alpha=0.6)

# Plot trendline
plt.plot(x, m * x + b, color="red", label="Trendline", linewidth=2)

# Titles and labels
plt.title("UN Contraceptive Use Percentage Data")
plt.xlabel("Year")
plt.ylabel("Contraceptive Use (%)")
plt.legend()
plt.show()
