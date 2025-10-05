import pandas as pd
import numpy as np
import scipy.stats as stats
import re

##################################################################
                    ## Helper Functions
##################################################################
def clear_data(string1):
    """Remove reference annotations like [8] from city names."""
    if re.search(r'\[[a-z]* [0-9]+\]', string1) is None:
        return string1
    else:
        return string1.replace(re.search(r'\[[a-z]* [0-9]+\]', string1).group(), '')
##################################################################
                    ## Load Data
##################################################################

# Load global data
nhl_df = pd.read_csv("assets/nhl.csv")
cities = pd.read_html("assets/wikipedia_data.html")[1]
cities = cities.iloc[:-1, [0, 3, 5, 6, 7, 8]]

# Clean Cities data
cities['NHL'] = cities['NHL'].apply(lambda x: clear_data(str(x)))
nhl_cities = cities[['Metropolitan area', 'NHL']].set_index('NHL')
nhl_cities = nhl_cities.drop(['—', ''], errors='ignore')

# Keep only NHL 2018 data
nhl_2018 = nhl_df[nhl_df['year'] == 2018].copy()


# Population data
population = cities[['Metropolitan area', 'Population (2016 est.)[8]']].set_index('Metropolitan area')
population['Population (2016 est.)[8]'] = pd.to_numeric(population['Population (2016 est.)[8]'].str.replace(',', ''))



def get_area(team):
    """Map an NHL team name to its corresponding metropolitan area."""
    for each in list(nhl_cities.index.values):
        if team in each:
            return nhl_cities.at[each, 'Metropolitan area']
        
# Clean NHL data
nhl_2018['team'] = nhl_2018['team'].apply(lambda x: x[:-1].strip() if str(x).endswith("*") else str(x).strip())
nhl_2018['Metropolitan area'] = nhl_2018['team'].apply(lambda x: get_area(x.split(" ")[-1]))

##################################################################
            ## Compute win/loss ratio per metro area
##################################################################

out = []
for group, frame in nhl_2018.groupby('Metropolitan area'):
    total_wins = frame['W'].astype(float).sum()
    total_losses = frame['L'].astype(float).sum()
    ratio = total_wins / (total_wins + total_losses)
    out.append({'Area': group, 'Ratio': ratio})

out_df = pd.DataFrame(out).set_index('Area')
out_df = out_df.merge(population, left_index=True, right_index=True, how='inner')

##################################################################
            ## Function to calculate correlation
##################################################################

def nhl_correlation():
    population_by_region = out_df['Population (2016 est.)[8]'].dropna()
    win_loss_by_region = out_df['Ratio'].dropna()
    
    # Align indices
    population_by_region, win_loss_by_region = population_by_region.align(win_loss_by_region, join='inner')
    
    assert len(population_by_region) == len(win_loss_by_region), "Lists must be the same length"
    assert len(population_by_region) == 28, "There should be 28 NHL teams analysed"
    
    corr_tup = stats.pearsonr(population_by_region, win_loss_by_region)  # return only correlation coefficient
    return corr_tup[0]
nhl_correlation()
