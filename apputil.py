#-----IMPORTS-----#
import pandas as pd
import numpy as np
import streamlit as st
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
    age_bins = [0, 13, 20, 60, np.inf]
    age_labels = ["Child", "Teen", "Adult", "Senior"]

    df_titanic['Age_Group'] = pd.cut(
            df_titanic['Age'], 
            bins = age_bins, 
            labels = age_labels, 
            right = False, 
            include_lowest = True
        )

    #create new by after filitering df_titanic for the data that we need. Main attributes Class, Sex, and Age Group
    demographics = df_titanic.groupby(['Pclass', 'Sex', 'Age_Group'], observed = True).agg(
            #calculate number of passengers, ensure that they exist
            n_passengers=('PassengerId', 'count'), 
            #calculate number of survivors, sum total
            n_survivors=('Survived', 'sum')
        ).reset_index()



    #adding new attributes, survival rate
    demographics['survival_rate'] = demographics['n_survivors'] / demographics['n_passengers']
    
    #create table ordered from high survival rate, to low survival rate
    demographics = demographics.sort_values(by = 'survival_rate', ascending = False)
    
    return demographics



def visualize_demographic(df_demographics):











#--------------------#
#-----MAIN-----#
#debuge code
#print(survival_demographics(df_titanic))

st.write("something something")
visualize_demographic(survival_demographics(df_titanic))