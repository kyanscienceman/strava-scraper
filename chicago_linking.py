import pandas as pd
import numpy as numpy
import jellyfish
import datetime
import time

### NOTE: I have named this file chicago_linking, but it most likely can be used for linking any marathon considering we format all of our scrapes the same way

RACE_DICT = {'CH14': ['ChicagoOfficial2014.csv', 'strava_chicago_2014.csv']} 

def create_marathon_df(raceID):
    '''
    Takes in the csv file of a race's results scraped from the marathon website and turns it into a useable dataframe object

    Inputs:
        filename (string) name of the file we want to turn into a df
    Returns:
        marathon_df (DataFrame) 
    '''

    filename = RACE_DICT[raceID][0]

    marathon_df = pd.read_csv(filename, header=None) #read without a header because the first row of csv contains real data
    marathon_df.columns = ['Name', 'Gender_and_Age', 'Time']
    marathon_df['Gender'] = marathon_df.gender_and_age.str[0]
    marathon_df['Age'] = marathon_df.gender_and_age.str[1:]
    marathon_df = marathon_df.drop['Gender_and_Age']
    marathon_df['RaceID'] = raceID
    cols = ['RaceID', 'Name', 'Gender', 'Age']

    return marathon_df

def create_strava_df(raceID):
    '''
    Takes in the csv file of a race's results scraped from strava and turns it into a useable dataframe objects.

    Inputs:
        filename (string) name of the file we want to turn into a df
    Returns:
        strava_df_list (list) list of DataFrame objects 
    '''

    filename = RACE_DICT[raceID][1]

    strava_df = pd.read_csv(filename, sep='|')

    return strava_df

def create_dataframes(raceID):

    marathon_df = create_marathon_df(raceID)
    strava_df = create_strava_df(raceID)

    for s_label, s_row in strava_df.iterrows():
        for m_label, m_row in marathon_df.iterrows():
            strava_name = s_row[1]
            marathon_name = m_row[0]
            strava_time = s_row[4]
            marathon_time = m_row[2]

            marathon_time_obj = time.strptime(marathon_time, '%H:%M:%S')
            marathon_hour = marathon_time_obj.tm_hour
            marathon_min = marathon_time_obj.tm_min / 60
            marathon_time = marathon_hour + marathon_min

            strava_time_obj = time.strptime(strava_time, '%H:%M:%S')
            strava_hour = strava_time_obj.tm_hour
            strava_min = strava_time_obj.tm_min / 60
            strava_time = strava_hour + strava_min

            name_score = jellyfish.jaro_winkler(strava_name, marathon_name)
            time_diff = marathon_time - strava_time

            #Compare the name_score and time_diff and determine if we want this as a match or nonmatch, then store the indexes

    #Take indexes and append the rows from each dataframe according to those indexes

