import pandas as pd
import numpy as np
import scipy.stats as stats
import re

nhl_df=pd.read_csv("assets/nhl.csv")
cities=pd.read_html("assets/wikipedia_data.html")[1]
cities=cities.iloc[:-1,[0,3,5,6,7,8]]
nhl_2018 = nhl_df.head(35)

## Clean Cities dataframe
cities_modified = cities.drop(['NFL', 'MLB', 'NBA'], axis=1)
cities_modified["NHL"] = cities_modified["NHL"].str.replace(r"\[.*?\]", "", regex=True).str.strip()

# Ensure GP is numeric (filters out any leftover header rows)
nhl_2018 = nhl_2018[pd.to_numeric(nhl_2018["GP"], errors="coerce").notna()]

# Reset the index
nhl_2018 = nhl_2018.reset_index(drop=True)

# Create Win/Loss Ratio
nhl_2018["W"] = pd.to_numeric(nhl_2018["W"], errors="coerce").astype("Int64")
nhl_2018["L"] = pd.to_numeric(nhl_2018["L"], errors="coerce").astype("Int64")
nhl_2018["W/L"] = nhl_2018["W"] / nhl_2018["L"]

nhl_2018["team"] = nhl_2018["team"].str.replace(r"\*$", "", regex=True).str.strip()

Cities_Series = cities_modified["Metropolitan area"]

# Clean Cities_Series for matching
Cities_Cleaned = (
    Cities_Series.str.replace(r"[\.,]", "", regex=True)       # remove punctuation
                 .str.replace(r"\s+Area$", "", regex=True)   # remove 'Area'
                 .str.replace(r"\s+–.*", "", regex=True)     # remove ranges
                 .str.strip()
)

# Only keep city names that actually match the start of some team
mask = Cities_Cleaned.apply(lambda city: nhl_2018["team"].str.startswith(city).any())
Cities_To_Remove = Cities_Cleaned[mask]

# Build regex pattern dynamically
pattern = r"^(?:" + "|".join(map(re.escape, Cities_To_Remove)) + r")\s*"

# Remove city names from NHL teams (vectorized)
nhl_2018["team"] = nhl_2018["team"].str.replace(pattern, "", regex=True).str.strip()
def show_wiki():

    return cities_modified

def show_df():

    return nhl_2018['team']

def nhl_correlation(): 
    population_by_region = [] # pass in metropolitan area population from cities
    win_loss_by_region = [] # pass in win/loss ratio from nhl_df in the same order as cities["Metropolitan area"]
    assert len(population_by_region) == len(win_loss_by_region), "Q1: Your lists must be the same length"
    assert len(population_by_region) == 28, "Q1: There should be 28 teams being analysed for NHL"
    
show_df()
