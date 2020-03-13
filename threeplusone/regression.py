'''
~~~3+1~~~
This file contains the necessary code to run the regressions and 
visualizations.
'''
import sys
import pandas as pd  
import numpy as np  
import matplotlib.pyplot as plt  
from sklearn.linear_model import LinearRegression
import datetime

CHECKS = ["%", "vf", "next", "vapor", " fly ", "vapour", "percent"]

RACES = ["BS", "BS14", "BS15", "BS16", "BS17", "BS18", "BS19", \
"NY", "NY14", "NY15", "NY16", "NY17", "NY18", "NY19", \
"CH", "CH14", "CH15", "CH16", "CH17", "CH18", "CH19"]

SEXES = ["M", "F"]

MASTER_MATCHES = "../scraping/race_result/master_matches.csv"

IMAGE_PATH = "strava/static/images/{}"

'''
Dataframe with Vaporfly identified in new column:
True for Vaporfly, False for non-Vaporfly shoes,
and None for no shoes inputted in Strava
'''

marathon_df = pd.read_csv(MASTER_MATCHES, sep=",")
marathon_df = marathon_df.dropna()
marathon_df["Vaporfly"] = marathon_df["Shoes"].apply(
    lambda s: any([check in s.lower() for check in CHECKS]))


def sec_to_hour(sec):
    '''
    Convert seconds to hours:minutes:seconds

    Input:
        s (int): seconds

    Output:
        string in the format H:M:S
    '''
    return str(datetime.timedelta(seconds = int(sec)))

def hour_to_sec(hms_str):
    '''
    Convert hours:minutes:seconds to seconds

    Inputs:
        hms_str (string): string formatted like H:M:S

    Returns:
        time in seconds
    '''
    h,m,s = hms_str.split(":")
    return int(h) * 3600 + int(m) * 60 + int(s)

def regressions(marathon_df=marathon_df, race=None, sex=None, age=None, time=None):
    '''
    Function that takes in various demographic data points input
    by the user to calculate a coefficient and estimate how much
    faster Vaporflies would make them run. We use a log 
    transformation on time prior to our regression to account for 
    diminishing returns on time the faster you get.

    Inputs:
        race (string): name of race (and year if you want to be
                        specific)
        sex (string): "M" for male and "F" for female
        age (int): age of the user
        time (str): time to complete a marathon, inputted as HH:MM:SS

    Returns:
        (float) Regression coefficient
        and saves two .png files
    '''
    param_str = ""
    if race is not None:
        assert race in RACES
        marathon_df = marathon_df[marathon_df["RaceID"] == race]
        param_str += ", " + race
    if age is not None:
        marathon_df = marathon_df[(marathon_df["Age_Lower"] <= age) & \
        (marathon_df["Age_Upper"] >= age)]
        param_str += ", " + "Age={}".format(age)
    if sex is not None:
        assert sex in SEXES
        marathon_df = marathon_df[marathon_df["Gender"] == sex]
        param_str += ", " + "Sex={}".format(sex)        

    #Running the regression
    marathon_df["Vaporfly"].astype("category") # change to categorical variables
    marathon_df["logTime"] = np.log(marathon_df["Time"]) # log transformation
    X = marathon_df["Vaporfly"].values.reshape(-1, 1)
    y = marathon_df["logTime"].values.reshape(-1, 1)
    reg = LinearRegression()
    reg.fit(X, y)
    beta0 = np.exp(reg.intercept_[0])
    beta1 = np.exp(reg.coef_[0][0])
    print("The linear model is: Y = {:.5} + {:.5}X"\
        .format(beta0 , beta1))

    if time is not None:
        time = hour_to_sec(time)
        newtime = time * beta1
        percent = (1 - newtime / time) * 100
        time = sec_to_hour(time)
        newtime = sec_to_hour(newtime)
        print("If you bought the Vaporflies, you would improve your time from",\
        "{} to {}, decreasing your finish time by {} percent".format(time, newtime, percent))

    #Scatter plot and regression line
    predictions = reg.predict(X)
    plt.figure(figsize=(16, 8))
    plt.scatter(marathon_df["Vaporfly"], marathon_df["logTime"], c="black")
    plt.plot(marathon_df["Vaporfly"], predictions, c="blue", linewidth=2)
    plt.xlabel("Presence of Vaporfly")
    plt.ylabel("Marathon Times")
    plt.title('Marathon Finish Time vs. Presence of Vaporfly{}'.format(param_str))
    plt.savefig(IMAGE_PATH.format("linearfit.png"))

    #Histograms
    marathon_df_y_vf = marathon_df[marathon_df["Vaporfly"] == True]
    y_vf = marathon_df_y_vf["Time"].values.reshape(-1,1)

    marathon_df_y_no_vf = marathon_df[marathon_df["Vaporfly"] == False]
    y_no_vf = marathon_df_y_no_vf["Time"].values.reshape(-1,1)

    num_bins = 100
    fig, ax = plt.subplots(figsize=(16, 8))
    n, bins, patches = ax.hist(y_vf, num_bins, density=1, label="VF",\
        histtype="barstacked", rwidth=0.5)
    n, bins, patches = ax.hist(y_no_vf, num_bins, density=1, label="No VF",\
        histtype="barstacked", rwidth=0.5)
    ax.legend(loc='upper right')
    ax.set_xlabel('Frequency of Finish Times (in seconds)')
    ax.set_ylabel('Probability Density')
    ax.set_title('Histogram of Marathon Finish Times{}'.format(param_str))
    plt.savefig(IMAGE_PATH.format("hist.png"))

    #Return coefficient on Vaporfly indicator
    return beta1

def find_runner(name):
    '''
    Function that takes in various demographic data points given a
    runner's name and returns how much faster they would have ran
    if they wore Vaporflys. Note: This works even if the runner is
    already wearing Vaporflys (e.g. it ignores prior shoe type).

    Inputs:
        name (string): name of runner

    Returns:
        (float) Regression coefficient
        and saves two .png files
    '''
    runner_df = marathon_df[marathon_df["Name"] == name]
    RaceID = runner_df.iloc[0,0]
    time = sec_to_hour(runner_df.iloc[0,2])
    sex = runner_df.iloc[0,3]
    avg_age = (runner_df.iloc[0,4] + runner_df.iloc[0,5])/2

    return regressions(marathon_df, race=RaceID, sex=sex, age=avg_age, time=time)

def return_runners_of_multiple_races():
    df = marathon_df[maraton_df.groupby("Name")["Name"].transform("size") > 1]
    df = df.sort_values(by="Name")
    return df


if __name__=="__main__":
    age = sys.argv[1]
    sex = sys.argv[2]
    time = sys.argv[3]
    regressions(age=int(age), sex=sex, time=time)
