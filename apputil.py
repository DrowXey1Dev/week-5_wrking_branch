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

    #clean data to handle missing age values. Without this the bar chart breaks
    median_age = df_titanic['Age'].median()
    df_titanic['Age'] = df_titanic['Age'].fillna(median_age)

    #map Pclass to strings
    df_titanic['Pclass'] = df_titanic['Pclass'].map({1: 'First', 2: 'Second', 3: 'Third'})

    #create bins for ages and labels
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

    #assign new dataframe
    male_survival_df = df_demographics[df_demographics['Sex'] == 'male']

    #reaggregate for men only
    male_class_survival_rate = male_survival_df.groupby('Pclass', observed = True).agg(
        #total men who survived and total people on board
        total_male_passengers = ('n_passengers', 'sum'),
        total_male_survivors = ('n_survivors', 'sum')
    ).reset_index()
    
    male_class_survival_rate['male_survival_rate'] = \
        male_class_survival_rate['total_male_survivors'] / male_class_survival_rate['total_male_passengers']
    
    
    #for better visualization we can assign categories. 
    male_class_survival_rate['Pclass'] = pd.Categorical(
        male_class_survival_rate['Pclass'], 
        categories = ['First', 'Second', 'Third'], 
        ordered = True
    )

    #-------------------CHART LOGIC-------------------#

    #bar chart for represnting male data for our question
    bar_chart_male = px.bar(
        #set params for the bar chart, axis, title, labels, color, etc
        male_class_survival_rate,
        x = 'Pclass',
        y = 'male_survival_rate',
        text = 'male_survival_rate',
        title = 'Male Survival Rate by Passenger Class',
        labels = {
            'Pclass': 'Passenger Class',
            'male_survival_rate': 'Survival Rate'
        },
        color_discrete_sequence = ["#00ff73"]
    )

    return bar_chart_male









#--------------------#
#-----MAIN-----#
#debuge code
#print(survival_demographics(df_titanic))

st.write("How does class impact the survival rate of men?")
st.write("As we can see, as the class level drops, so does the survivability rate of male passengers.")
bar_chart_output = visualize_demographic(survival_demographics(df_titanic))
st.plotly_chart(bar_chart_output, use_container_width=True) 

print("---Bar Chart for the question ""How does class impact the survival rate of men""---")