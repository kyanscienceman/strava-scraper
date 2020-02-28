import pandas as pd
import numpy as numpy
import jellyfish
import datetime
import time

### NOTE: I have named this file chicago_linking, but it most likely can be used for linking any marathon considering we format all of our scrapes the same way

RACE_DICT = {
    'CH14': ['ChicagoOfficial2014.csv', 'strava_chicago_2014.csv'], 
    'CH15': ['ChicagoOfficial2014.csv', 'strava_chicago_2015.csv'], 
    'CH16': ['Chicago2016official.csv', 'strava_chicago_2016.csv'], 
    'CH17': ['Chicago2017official.csv', 'strava_chicago_2017.csv'],
    'CH18': ['Chicago2018official.csv', 'strava_chicago_2018.csv'],
    'CH19': ['Chicago2019official.csv', 'strava_chicago_2019.csv'],
    'NY17': ['NewYork2017official.csv', 'strava_newyork_2017.csv'],
    'NY18': ['NewYork2018official.csv', 'strava_newyork_2018.csv'],
    'NY19': ['NewYork2019official.csv', 'strava_newyork_2019.csv'],
    'BS14': ['Boston2014official.csv', 'strava_boston_2014.csv'],
    'BS15': ['Boston2015official.csv', 'strava_boston_2015.csv'],
    'BS16': ['Boston2016official.csv', 'strava_boston_2016.csv'],
    'BS17': ['Boston2017official.csv', 'strava_boston_2017.csv'],
    'BS18': ['Boston2018official.csv', 'strava_boston_2018.csv'],
    'BS19': ['Boston2019official.csv', 'strava_boston_2019.csv']} 

def create_marathon_df(raceID):
    '''
    Takes in the csv file of a race's results scraped from the marathon website and turns it into a useable dataframe object

    Inputs:
        filename (string) name of the file we want to turn into a df
    Returns:
        marathon_df (DataFrame) 
    '''

    filename = RACE_DICT[raceID][0] #need to standardize these names

    marathon_df = pd.read_csv(filename, header=None) #read without a header because the first row of csv contains real data
    marathon_df.columns = ['Name', 'Gender_and_Age', 'Time']
    marathon_df['Gender'] = marathon_df.gender_and_age.str[0]
    marathon_df['Age'] = marathon_df.gender_and_age.str[1:]
    marathon_df = marathon_df.drop['Gender_and_Age']
    marathon_df['RaceID'] = raceID
    cols = ['RaceID', 'Name', 'Gender', 'Age'] #trying to reorder rows here

    return marathon_df

def create_strava_df(raceID):
    '''
    Takes in the csv file of a race's results scraped from strava and turns it into a useable dataframe objects.

    Inputs:
        filename (string) name of the file we want to turn into a df
    Returns:
        strava_df_list (list) list of DataFrame objects 
    '''

    filename = RACE_DICT[raceID][1] #need to standardize these names

    strava_df = pd.read_csv(filename, sep='|')

    return strava_df

def create_matches(raceID, acceptable_time_diff, acceptable_name_diff):
    '''
    Takes in a race ID and returns a dataframe of acceptable matches based on a passed acceptable time difference score and an acceptable namedifference score

    Inputs:
        raceID: (str) ID of the race you'd like to get matches for
        acceptable_time_diff (int) difference in seconds that you'd still consider a match
        acceptable_name_diff (int) Between 0-1, acceptable jaro-winkler score
    Returns:
        matches
    '''

    marathon_df = create_marathon_df(raceID)
    strava_df = create_strava_df(raceID)

    s_match_indexes = []
    m_match_indexes = []

    for s_index, s_row in strava_df.iterrows():
        for m_index, m_row in marathon_df.iterrows():
            strava_name = s_row[1]
            marathon_name = m_row[0]
            strava_time = s_row[4]
            marathon_time = m_row[2]

            marathon_time_obj = time.strptime(marathon_time, '%H:%M:%S')
            marathon_hour = marathon_time_obj.tm_hour
            marathon_min = marathon_time_obj.tm_min
            marathon_sec = marathon_time_obj.tm_sec
            marathon_time = (marathon_hour * 3600) + (marathon_min * 60) + marathon_sec

            strava_time_obj = time.strptime(strava_time, '%H:%M:%S')
            strava_hour = strava_time_obj.tm_hour
            strava_min = strava_time_obj.tm_min
            strava_sec = strava_time_obj.tm_sec
            strava_time = (strava_hour * 3600) + (strava_min * 60) + strava_sec

            name_score = jellyfish.jaro_winkler(strava_name, marathon_name)
            time_diff = marathon_time - strava_time #Calculates seconds diff

            if (name_score >= acceptable_name_diff and time_diff <= acceptable_time_diff):
                s_match_indexes.append(s_index)
                m_match_indexes.append(m_index)

    s_matches_half = strava_df.loc[s_match_indexes, :]
    s_matches_half.columns = 

    #Take indexes and append the rows from each dataframe according to those indexes

