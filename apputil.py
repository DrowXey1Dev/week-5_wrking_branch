#-----IMPORTS-----#
import pandas as pd
import numpy as np
import plotly.express as px

#-----PREP-----#
try:
    df_titanic = pd.read_csv('https://raw.githubusercontent.com/leontoddjohnson/datasets/main/data/titanic.csv')
except FileNotFoundError:
    print("ERROR. Specified dataset not found. Program will now crash :( ")





#--------------------#
#-----FUNCTION DEFS-----#
def survival_demographics(df_titanic):
    #debug code
    #print(df_titanic.info)
    age_bins = [0, 13, 20, 60]
    age_labels = ["Child", "Teen", "Adult", "Senior"]

    df_titanic['Age_Group'] = pd.cut(
            df_titanic['Age'], 
            bins = age_bins, 
            labels = age_labels, 
            right = False, 
            include_lowest = True
        )











#--------------------#
#-----MAIN-----#
survival_demographics(df_titanic)