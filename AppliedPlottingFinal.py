import pandas as pd
import numpy as np
import matplotlib as plt

## Load Data

female_homicide_df = pd.read_excel(r"C:\Users\kensi\Downloads\Intentional homicide victims by sex, counts and ra.xls", skiprows = 1)
female_homicide_cleaned_df = female_homicide_df[female_homicide_df['Sex'] == 'Female']

year_columns = [str(year) for year in range(2000, 2024)]

female_homicide_rates_df = pd.DataFrame()
female_homicide_rates_df["Country"] = female_homicide_cleaned_df["Country"]

for year in year_columns:
    count_col = year        # deaths
    rate_col = year + '.1'  # rate per 100,000
    pop = 0
    # Only calculate if both columns exist in the dataset
    if count_col in female_homicide_cleaned_df.columns and rate_col in female_homicide_cleaned_df.columns:
        # Convert rate per 100k into percentage
        pop = (female_homicide_cleaned_df[count_col] * 100000) / female_homicide_cleaned_df[rate_col]
        female_homicide_rates_df[year] = (female_homicide_cleaned_df[count_col] / pop) * 100
    else:
        female_homicide_rates_df[year] = np.nan


contraceptive_prevalence_df = pd.read_excel(r"C:\Users\kensi\Downloads\Contraceptive Prevalence Method.xls")
print(female_homicide_rates_df)
