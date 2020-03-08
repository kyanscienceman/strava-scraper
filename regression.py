'''
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
%matplotlib inline

races = ["BS", "BS14", "BS15", "BS16", "BS17", "BS18", "BS19", \
"NY", "NY14", "NY15", "NY16", "NY17", "NY18", "NY19", \
"CH", "CH14", "CH15", "CH16", "CH17", "CH18", "CH19"]

sexes = ["M", "F"]

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
    assert race in races
    assert sex in sexes

    marathon_df = pd.read_csv(filename)

    if race is not None:
        marathon_df = marathon_df["RaceID"] == race
    if sex is not None:
        marathon_df = marathon_df["Gender"] == sex
    if age is not None:
        marathon_df = marathon_df["Age"] == age

    X = marathon_df["Vaporflies"].values.reshape(-1,1)
    y = marathon_df["Time"].values.reshape(-1,1)

    reg = LinearRegression()
    reg.fit(X, y)
    
    print("The linear model is: Y = {:.5} + {:.5}X".format(reg.intercept_[0], \
     reg.coef_[0][0]))
    
    X2 = sm.add_constant(X)
    est = sm.OLS(y, X2)
    est2 = est.fit()
    print(est2.summary())

    predictions = reg.predict(X)

    plt.figure(figsize=(16, 8))
    plt.scatter(
        data["Time"],
        data["Vaporflies"],
        c="black"
    )
    plt.plot(
    data["Vaporflies"],
    predictions,
    c="blue",
    linewidth=2
    )
    plt.xlabel("Presence of Vaporflies")
    plt.ylabel("Marathon Times")
    plt.show()