import pandas as pd
import scipy.stats as stats
import numpy as np

'''Question 1
Write a function called proportion_of_education which returns the proportion of children in the dataset who had a mother with the education levels equal to less than high school (<12), high school (12), more than high school but not a college graduate (>12) and college degree.

This function should return a dictionary in the form of (use the correct numbers, do not round numbers):

    {"less than high school":0.2,
    "high school":0.4,
    "more than high school but not college":0.2,
    "college":0.2}'''
def proportion_of_education():
    ## Pull CSV data into a dataframe
    df = pd.read_csv('assets/NISPUF17.csv')
    df_educ = df['EDUC1'].value_counts(normalize=True)
    
    ## Organize that data into a dictionary
    educ_dict = {
        "less than high school": df_educ.loc[1],
        "high school": df_educ.loc[2],
        "more than high school but not college": df_educ.loc[3],
        "college": df_educ.loc[4]
    }
    
    return educ_dict
'''Question 2
Let's explore the relationship between being fed breastmilk as a child and getting a seasonal influenza vaccine from a healthcare provider. Return a tuple of the average number of influenza vaccines for those children we know received breastmilk as a child and those who know did not.

This function should return a tuple in the form (use the correct numbers:

(2.5, 0.1)'''
def average_influenza_doses():
    ## Pull CSV data into a dataframe
    df = pd.read_csv('assets/NISPUF17.csv')
    
    # Children who were fed breastmilk
    milk_vacc = df.loc[df["CBF_01"] == 1, "P_NUMFLU"].mean()
    
    # Children who were not fed breastmilk
    no_milk_vacc = df.loc[df["CBF_01"] == 2, "P_NUMFLU"].mean()
    
    return (milk_vacc, no_milk_vacc)
'''Question 3
It would be interesting to see if there is any evidence of a link between vaccine effectiveness and sex of the child. Calculate the ratio of the number of children who contracted chickenpox but were vaccinated against it (at least one varicella dose) versus those who were vaccinated but did not contract chicken pox. Return results by sex.

This function should return a dictionary in the form of (use the correct numbers):

    {"male":0.2,
    "female":0.4}
Note: To aid in verification, the chickenpox_by_sex()['female'] value the autograder is looking for starts with the digits 0.0077.'''
def chickenpox_by_sex():
    df = pd.read_csv('assets/NISPUF17.csv')

    # Males
    male_had = df[(df['SEX'] == 1) & (df['HAD_CPOX'] == 1) & (df['P_NUMVRC'] >= 1)].shape[0]
    male_no = df[(df['SEX'] == 1) & (df['HAD_CPOX'] == 2) & (df['P_NUMVRC'] >= 1)].shape[0]
    male_ratio = male_had / male_no

    # Females
    female_had = df[(df['SEX'] == 2) & (df['HAD_CPOX'] == 1) & (df['P_NUMVRC'] >= 1)].shape[0]
    female_no = df[(df['SEX'] == 2) & (df['HAD_CPOX'] == 2) & (df['P_NUMVRC'] >= 1)].shape[0]
    female_ratio = female_had / female_no

    return {"male": male_ratio, "female": female_ratio}
'''
Question 4
A correlation is a statistical relationship between two variables. If we wanted to know if vaccines work, we might look at the correlation between the use of the vaccine and whether it results in prevention of the infection or disease [1]. In this question, you are to see if there is a correlation between having had the chicken pox and the number of chickenpox vaccine doses given (varicella). Some notes on interpreting the answer. The had_chickenpox_column is either 1 (for yes) or 2 (for no), and the_num_chickenpox_vaccine_column is the number of doses a child has been given of the varicella vaccine. A positive correlation (e.g., corr > ◊ ) means that an increase in had_chickenpox_column (which means more no's) would also increase the values of num_chickenpox_vaccine_column (which means more doses of vaccine). If there is a negative correlation (e.g., corr < 0), it indicates that having had chickenpox is related to an increase in the number of vaccine doses.
Also, pval is the probability that we observe a correlation between had_chickenpox_column_and_num_chickenpox_vaccine_column which is greater than or equal to a particular value occurred by chance. A small pval means that the observed correlation is highly unlikely to occur by chance. In this case, pval should be very small (will end in e-18 indicating a very small number).
[1] This isn't really the full picture, since we are not looking at when the dose was given. It's possible that children had chickenpox and then their parents went to get them the vaccine. Does this dataset have the data we would need to investigate the timing of the dose?'''
def corr_chickenpox():
    
    # Load dataset
    df = pd.read_csv("assets/NISPUF17.csv")
    
    # Select needed columns
    df = df[["HAD_CPOX", "P_NUMVRC"]]
    
    # Drop rows with invalid/missing values
    df = df[(df["HAD_CPOX"].isin([1, 2])) & (df["P_NUMVRC"] >= 0)]
    
    # Calculate Pearson correlation
    corr, pval = stats.pearsonr(df["HAD_CPOX"], df["P_NUMVRC"])
    
    return corr
