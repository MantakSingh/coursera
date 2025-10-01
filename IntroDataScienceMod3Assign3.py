import pandas as pd
import numpy as np
import re

'''### Question 1
Load the energy data from the file `assets/Energy Indicators.xls`, which is a list of indicators of [energy supply and renewable electricity production](assets/Energy%20Indicators.xls) from the [United Nations](http://unstats.un.org/unsd/environment/excel_file_tables/2013/Energy%20Indicators.xls) for the year 2013, and should be put into a DataFrame with the variable name of **Energy**.

Keep in mind that this is an Excel file, and not a comma separated values file. Also, make sure to exclude the footer and header information from the datafile. The first two columns are unneccessary, so you should get rid of them, and you should change the column labels so that the columns are:

`['Country', 'Energy Supply', 'Energy Supply per Capita', '% Renewable]`

Convert `Energy Supply` to gigajoules (**Note: there are 1,000,000 gigajoules in a petajoule**). For all countries which have missing data (e.g. data with "...") make sure this is reflected as `np.NaN` values.

Rename the following list of countries (for use in later questions):

```"Republic of Korea": "South Korea",
"United States of America": "United States",
"United Kingdom of Great Britain and Northern Ireland": "United Kingdom",
"China, Hong Kong Special Administrative Region": "Hong Kong"```

There are also several countries with parenthesis in their name. Be sure to remove these, e.g. `'Bolivia (Plurinational State of)'` should be `'Bolivia'`. Additionally, there are several countries with Numeric digits in their name. Make sure to remove these as well, e.g. `'Italy9'` should be `'Italy'`. 

Next, load the GDP data from the file `assets/world_bank.csv`, which is a csv containing countries' GDP from 1960 to 2015 from [World Bank](http://data.worldbank.org/indicator/NY.GDP.MKTP.CD). Call this DataFrame **GDP**. 

Make sure to skip the header, and rename the following list of countries:

```"Korea, Rep.": "South Korea", 
"Iran, Islamic Rep.": "Iran",
"Hong Kong SAR, China": "Hong Kong"```

Finally, load the [Sciamgo Journal and Country Rank data for Energy Engineering and Power Technology](http://www.scimagojr.com/countryrank.php?category=2102) from the file `assets/scimagojr-3.xlsx`, which ranks countries based on their journal contributions in the aforementioned area. Call this DataFrame **ScimEn**.

Join the three datasets: GDP, Energy, and ScimEn into a new dataset (using the intersection of country names). Use only the last 10 years (2006-2015) of GDP data and only the top 15 countries by Scimagojr 'Rank' (Rank 1 through 15). 

The index of this DataFrame should be the name of the country, and the columns should be ['Rank', 'Documents', 'Citable documents', 'Citations', 'Self-citations',
       'Citations per document', 'H index', 'Energy Supply',
       'Energy Supply per Capita', '% Renewable', '2006', '2007', '2008',
       '2009', '2010', '2011', '2012', '2013', '2014', '2015'].

*This function should return a DataFrame with 20 columns and 15 entries, and the rows of the DataFrame should be sorted by "Rank".*'''

def answer_one():
       
    ##################################################################
                        ## Energy Dataframe
    ##################################################################
    Energy = pd.read_excel("assets/Energy Indicators.xls", skiprows=17, usecols="C:F")
    Energy = Energy.dropna(how="all")
    Energy.columns = ["Country", "Energy Supply", "Energy Supply per Capita", "% Renewable"]
    
    ## Cleaning Data
    Energy["Energy Supply"].replace(r"\.{3,}", np.nan, regex=True, inplace=True)
    Energy['Energy Supply'] *= 1000000
    
    ## Changing country names
    Energy.replace(r"Republic of Korea", "South Korea", regex=True, inplace=True)
    Energy.replace(r"United States of America", "United States", regex=True, inplace=True)
    Energy.replace(r"United Kingdom of Great Britain and Northern Ireland", "United Kingdom", regex=True, inplace=True)
    Energy.replace(r"China, Hong Kong Special Administrative Region", "Hong Kong", regex=True, inplace=True)
    Energy.replace(r"[0-9]", "" , regex=True, inplace=True)
    Energy["Country"].replace(r"[()]", "", regex=True, inplace=True)
    
    ##################################################################
                        ## GDP Dataframe
    ##################################################################
    
    GDP = pd.read_csv("assets/world_bank.csv", skiprows=4)
    GDP.rename(columns={"Country Name": "Country"}, inplace=True)
    GDP = GDP[['Country','2006','2007','2008','2009','2010','2011','2012','2013','2014','2015']]
    
    ## Changing country names
    GDP.replace(r"Korea, Rep.", "South Korea", regex=True, inplace=True)
    GDP.replace(r"Iran, Islamic Rep.", "Iran", regex=True, inplace=True)
    GDP.replace(r"Hong Kong SAR, China", "Hong Kong", regex=True, inplace=True)

    ##################################################################
                        ## ScimEn Dataframe
    ##################################################################    
    ScimEn = pd.read_excel("assets/scimagojr-3.xlsx")
    ScimEn = ScimEn.head(15)
    
    ##################################################################
                        ## Combined Dataframe
    ##################################################################    
    df = pd.merge(ScimEn, GDP, how='left', on='Country')
    df = pd.merge(df, Energy, how='left', on='Country')
    df.set_index('Country', inplace=True)
    df.columns = [
        'Rank', 'Documents', 'Citable documents', 'Citations', 'Self-citations', 'Citations per document', 
        'H index', 'Energy Supply', 'Energy Supply per Capita', 
        '% Renewable', '2006', '2007', '2008', '2009', '2010', '2011', '2012', '2013', '2014', '2015'
    ]
       
    return df
       
def answer_two():
       
    ##################################################################
                        ## Energy Dataframe
    ##################################################################
    
    Energy = pd.read_excel('assets/Energy Indicators.xls',
                           na_values=["..."],header = None,
                           skiprows=18,
                           skipfooter= 38,
                           usecols=[2,3,4,5],
                           names=['Country', 'Energy Supply', 'Energy Supply per Capita', '% Renewable'])
    Energy['Energy Supply'] = Energy['Energy Supply'].apply(lambda x: x*1000000)

    Energy['Country'] = Energy['Country'].str.replace(r" \(.*\)","")
    Energy['Country'] = Energy['Country'].str.replace(r"\d*","")
    Energy['Country'] = Energy['Country'].replace(
        {'Republic of Korea' : 'South Korea',
         'United States of America' : 'United States',
         'United Kingdom of Great Britain and Northern Ireland':'United Kingdom',
         'China, Hong Kong Special Administrative Region':'Hong Kong'
        })
    
    ##################################################################
                        ## GDP Dataframe
    ##################################################################
    
    GDP = pd.read_csv('assets/world_bank.csv', skiprows = 4)
    GDP['Country Name'] = GDP['Country Name'].replace(
        {'Korea, Rep.': 'South Korea', 
         'Iran, Islamic Rep.': 'Iran', 
         'Hong Kong SAR, China' : 'Hong Kong'})
    GDP.rename(columns = {"Country Name":"Country"},inplace=True)
    GDP = GDP.loc[:,['2006', '2007', '2008', '2009', '2010', '2011', '2012', '2013', '2014', '2015',"Country"]]
       
    ##################################################################
                        ## ScimEn Dataframe
    ##################################################################
    
    ScimEn = pd.read_excel('assets/scimagojr-3.xlsx')
    
    ##################################################################
                        ## Combined Dataframe
    ##################################################################
    
    inner1 = pd.merge(ScimEn,Energy,how="inner",left_on="Country",right_on="Country")
    inner2 = pd.merge(inner1,GDP,how="inner",left_on="Country",right_on="Country").set_index("Country")

    outer1 = pd.merge(ScimEn,Energy,how="outer",left_on="Country",right_on="Country")
    outer2 = pd.merge(outer1,GDP,how="outer",left_on="Country",right_on="Country").set_index("Country")

    return len(outer2)-len(inner2)
