'''
filename = "../race_result/test_ny19.csv"
~~~3+1~~~
This file contains the necessary code to run the regressions and 
visualizations.
'''
import pandas as pd  
import numpy as np  
import matplotlib.pyplot as plt  
from matplotlib import pyplot
import seaborn as seabornInstance 
from sklearn.model_selection import train_test_split 
from sklearn.linear_model import LinearRegression
from sklearn import metrics
import statsmodels.formula.api as smf
from statsmodels.iolib.summary2 import summary_col
import statsmodels.api as sm
from statsmodels.formula.api import ols
import datetime
#%matplotlib inline

CHECKS = ["%", "vf", "next", "vapor", " fly ", "vapour", "percent"]

RACES = ["BS", "BS14", "BS15", "BS16", "BS17", "BS18", "BS19", \
"NY", "NY14", "NY15", "NY16", "NY17", "NY18", "NY19", \
"CH", "CH14", "CH15", "CH16", "CH17", "CH18", "CH19"]

SEXES = ["M", "F"]

def convert_seconds_to_hours(sec):
    '''
    Convert seconds to hours:minutes:seconds

    Input:
        s (int): seconds

    Output:
        string hours:minutes:seconds
    '''
    return str(datetime.timedelta(seconds = sec))

def convert_hours_to_seconds(string):
    h,m,s = string.split(":")
    return int(h) * 3600 + int(m) * 60 + int(s)

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
        marathon_df = marathon_df[(marathon_df["Age_Lower"] <= age) & \
        (marathon_df["Age_Upper"] >= age)]

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
    marathon_df = pd.read_csv(filename, sep=",")
    marathon_df = marathon_df.dropna()
    marathon_df["Vaporfly"] = marathon_df["Shoes"].apply(
        lambda s: any([check in s.lower() for check in CHECKS]))

    return marathon_df


def regressions(filename, race=None, sex=None, age=None, time=None):
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
        time (str): time to complete a marathon, inputted as HH:MM:SS

    Returns:
        plots: histogram and regression
        regression output
    '''
    marathon_df = find_vaporfly(filename)


    if race is not None:
        assert race in RACES
        marathon_df = marathon_df[marathon_df["RaceID"] == race]
    if sex is not None:
        assert sex in SEXES
        marathon_df = marathon_df[marathon_df["Gender"] == sex]
    if age is not None:
        marathon_df = marathon_df[(marathon_df["Age_Lower"] <= age) & \
        (marathon_df["Age_Upper"] >= age)]


    marathon_df["Vaporfly"].astype("category") # change to categorical variables
    X = marathon_df["Vaporfly"].values.reshape(-1,1)
    y = marathon_df["Time"].values.reshape(-1,1)

    reg = LinearRegression()
    res = reg.fit(X, y)
    
    print("The linear model is: Y = {:.5} + {:.5}X".format(reg.intercept_[0], \
     reg.coef_[0][0]))

    improvement = reg.coef_[0][0]

    # fix time code Can't convert 'numpy.float64' object to str implicitly
    if time is not None:
        time = convert_hours_to_seconds(time)
        newtime = time + improvement
        percent = (1-newtime/time)*100
        time = convert_seconds_to_hours(time)
        newtime = convert_seconds_to_hours(newtime)
        print("If you bought the Vaporflies, you would improve your time from", \
        "{} to {}, increasing your finish time by {} percent".format(time, newtime, \
            percent))
    
    # fit = ols('y ~ C(X)', data=marathon_df).fit()
    # fit.summary()

    predictions = reg.predict(X)
    
    plt.figure(figsize=(16, 8))
    plt.scatter(
        marathon_df["Vaporfly"],
        marathon_df["Time"],
        c="black"
    )
    
    plt.plot(
    marathon_df["Vaporfly"],
    predictions,
    c="blue",
    linewidth=2
    )

    plt.xlabel("Presence of Vaporfly")
    plt.ylabel("Marathon Times")
    plt.show()

    # print out histograms
    marathon_df_y_vf = marathon_df[marathon_df["Vaporfly"] == True]
    y_vf = marathon_df_y_vf["Time"].values.reshape(-1,1)

    marathon_df_y_no_vf = marathon_df[marathon_df["Vaporfly"] == False]
    y_no_vf = marathon_df_y_no_vf["Time"].values.reshape(-1,1)

    num_bins = 100
    fig, ax = plt.subplots(figsize=(16, 8))
    n, bins, patches = ax.hist(y_vf, num_bins, density=1, label="VF", histtype="barstacked")
    n, bins, patches = ax.hist(y_no_vf, num_bins, density=1, label="No VF", histtype="barstacked")
    ax.legend(loc='upper right')
    ax.set_xlabel('Frequency of Finish Times')
    ax.set_ylabel('Probability Density')
    ax.set_title(r'Histogram of Marathon Finish Times')
