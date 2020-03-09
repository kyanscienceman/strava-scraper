'''
filename = "../race_result/test_ny19.csv"
~~~3+1~~~
This file contains the necessary code to run the regressions and 
visualizations.
'''
import pandas as pd  
import numpy as np  
import matplotlib.pyplot as plt  
import seaborn as seabornInstance 
from sklearn.model_selection import train_test_split 
from sklearn.linear_model import LinearRegression
from sklearn import metrics
#import statsmodels.api as sm
#%matplotlib inline

CHECKS = ["%", "vf", "fly", "next", "vapor", "vapour", "percent"]

RACES = ["BS", "BS14", "BS15", "BS16", "BS17", "BS18", "BS19", \
"NY", "NY14", "NY15", "NY16", "NY17", "NY18", "NY19", \
"CH", "CH14", "CH15", "CH16", "CH17", "CH18", "CH19"]

SEXES = ["M", "F"]

def average_marathon_time(race=None, sex=None, age=None):
    '''
    Testing function to see if we can display information on Django site
    Returns average marathon time of subset of runners specified
    by the above inputs (race, sex, age)
    
    Inputs:
        race (string): name of race
        sex (string): "M" or "F"
        age (int): age of the user
    '''
    #Very, very temporarily just do it for NY19 lmaooo
    marathon_df = pd.read_csv("../race_result/test_ny19.csv", delimiter='|')

    if race is not None:
        assert race in RACES
        marathon_df = marathon_df[marathon_df["RaceID"] == race]
    if sex is not None:
        assert sex in SEXES
        marathon_df = marathon_df[marathon_df["Gender"] == sex]
    if age is not None:
        marathon_df = marathon_df[(marathon_df["Age_Lower"] <= age) & (marathon_df["Age_Upper"] >= age)]

    return marathon_df["Time"].mean()


def find_vaporfly(filename):
    '''
    Inputs:
        filename (string): name of file
    Returns:
        dataframe (df): dataframe with Vaporfly identified in new column
            identification as True for Vaporfly, False for non-Vaporfly shoes
            and None for no shoes inputted in Strava

    '''
    marathon_df = pd.read_csv(filename, sep="|")
    marathon_df["Vaporfly"] = None
    row_count = marathon_df.shape[0]

    for i in range(row_count):
        shoe = marathon_df.iloc[i,7]
        vaporfly = marathon_df.iloc[i,8]
        # shoes will temporarily be 6th column
        # vaporfly will temporarily be 7th column
        if pd.isnull(shoe) is False:
            marathon_df.iloc[i,8] = False
            for check in CHECKS:
                if marathon_df.iloc[i,8] is False:
                    if check in shoe.lower():
                        marathon_df.iloc[i,8] = True
    return marathon_df


def regressions(filename, race=None, sex=None, age=None, time=False):
    '''
    Function that takes in a filename and various demographic
    data points inputted by the user to spit out a coefficient and
    estimation on how much faster Vaporflies would make you.

    Inputs:
        filename (string): name of file
        race (string): name of race (and year if you want to be
                        specific)
        sex (string): "M" for male and "F" for female
        age (int): age of the user
        time (int): time to complete a marathon

    Returns:

    '''
    marathon_df = find_vaporfly(filename)

    if race is not None:
        assert race in RACES
        marathon_df = marathon_df[marathon_df["RaceID"] == race]
    if sex is not None:
        assert sex in SEXES
        marathon_df = marathon_df[marathon_df["Gender"] == sex]
    if age is not None:
        marathon_df = marathon_df[(marathon_df["Age_Lower"] <= age) & (marathon_df["Age_Upper"] >= age)]

    marathon_df = marathon_df.dropna() # drop NAs and last 50 rows for outliers
    marathon_df["Vaporfly"].astype("category") # change to categorical variables
    X = marathon_df["Vaporfly"].values.reshape(-1,1)
    y = marathon_df["Time"].values.reshape(-1,1)

    reg = LinearRegression()
    reg.fit(X, y)
    
    print("The linear model is: Y = {:.5} + {:.5}X".format(reg.intercept_[0], \
     reg.coef_[0][0]))
    
    # X2 = sm.add_constant(X)
    # est = sm.OLS(y, X2)
    # est2 = est.fit()
    # print(est2.summary())

    predictions = reg.predict(X)

    plt.figure(figsize=(16, 8))
    plt.scatter(
    	marathon_df["Vaporfly"],
        marathon_df["Time"],
        c="black"
    )
    # plt.plot(
    # marathon_df["Vaporfly"],
    # predictions,
    # c="blue",
    # linewidth=2
    # )
    plt.xlabel("Presence of Vaporfly")
    plt.ylabel("Marathon Times")
    plt.show()