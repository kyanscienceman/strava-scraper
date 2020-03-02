import math
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

    print(RACE_DICT[raceID][0])
    filename = "race_result/" + RACE_DICT[raceID][0] #need to standardize these names

    marathon_df = pd.read_csv(filename, header=None) #read without a header because the first row of csv contains real data
    marathon_df.columns = ['Name', 'Gender_and_Age', 'Time']
    marathon_df['Gender'] = marathon_df['Gender_and_Age'].str[0]
    marathon_df['Age'] = marathon_df['Gender_and_Age'].str[1:]
    marathon_df = marathon_df.drop(columns=['Gender_and_Age'])
    marathon_df['RaceID'] = raceID
    marathon_df['Age_Lower'] = marathon_df['Age'].str.extract('(\d+)-')
    marathon_df['Age_Upper'] = marathon_df['Age'].str.extract('-(\d+)')

    marathon_df = convert_to_seconds(marathon_df)

    return marathon_df

def create_strava_df(raceID):
    '''
    Takes in the csv file of a race's results scraped from strava and turns it into a useable dataframe objects.

    Inputs:
        filename (string) name of the file we want to turn into a df
    Returns:
        strava_df_list (list) list of DataFrame objects 
    '''

    filename = "race_result/" + RACE_DICT[raceID][1] #need to standardize these names

    strava_df = pd.read_csv(filename, sep='|')
    strava_df['Time'] = strava_df['Time1']
    strava_df = strava_df.drop(columns=['Time1', 'Time2'])
    strava_df = strava_df[strava_df['Time'].str.contains("^\d:")]

    strava_df = convert_to_seconds(strava_df)
    strava_df['Age_Lower'] = strava_df['Age'].str.extract('(\d+)-')
    strava_df['Age_Upper'] = strava_df['Age'].str.extract('-(\d+)')
    #strava_df = strava_df[strava_df['Shoes'].isna() == False]

    return strava_df

def convert_to_seconds(df):
    '''
    Take in df and return it with the time column converted to seconds
    '''

    df['Time'] = df.apply(lambda row: time.strptime(row.loc['Time'], '%H:%M:%S'), axis=1)
    df['Time'] = df.apply(lambda row: row.loc['Time'].tm_hour * 3600 + row.loc['Time'].tm_min * 60 + row.loc['Time'].tm_sec, axis=1)

    return df

def create_matches(raceID, acceptable_name_score=0.85):
    '''
    Takes in a race ID and returns a dataframe of acceptable matches based on a passed acceptable time difference score and an acceptable namedifference score

    Inputs:
        raceID: (str) ID of the race you'd like to get matches for
        acceptable_time_diff (int) difference in seconds that you'd still consider a match
        acceptable_name_diff (int) Between 0-1, acceptable jaro-winkler score
    Returns:
        matches (DataFrame)
    '''

    marathon_df = create_marathon_df(raceID)
    strava_df = create_strava_df(raceID)

    s_match_indexes = []
    m_match_indexes = []

    for s_index, s_row in strava_df.iterrows():
        strava_time = s_row.at['Time']
        strava_name = s_row.at['Name']
        strava_gender = s_row.at['Gender']
        strava_age_lower = s_row.at['Age_Lower']
        strava_age_upper = s_row.at['Age_Upper']

        strava_age_present = isinstance(strava_age_lower, str)
        if strava_age_present:
            strava_age_lower = int(strava_age_lower)
            strava_age_upper = int(strava_age_upper)

        searchable_marathon_df = marathon_df[(marathon_df['Time'] <= strava_time + 60) & (marathon_df['Time'] >= strava_time - 60) & (marathon_df['Gender'] == strava_gender)]
        
        for m_index, m_row in searchable_marathon_df.iterrows():
            marathon_age_lower = m_row.at['Age_Lower']
            marathon_age_upper = m_row.at['Age_Upper']
            if strava_age_present:
                marathon_age_lower = int(marathon_age_lower)
                marathon_age_upper = int(marathon_age_upper)
                if marathon_age_lower >= strava_age_upper or strava_age_lower >= marathon_age_upper:
                    continue

            print('s_index:', s_index, 'm_index:', m_index)
            marathon_name = m_row.at['Name']

            name_score = jellyfish.jaro_winkler(strava_name, marathon_name)
            if name_score >= acceptable_name_score:
                s_match_indexes.append(s_index)
                m_match_indexes.append(m_index)
                break

    matches = pd.concat([strava_df.loc[s_match_indexes].reset_index(drop=True), marathon_df.loc[m_match_indexes].reset_index(drop=True)], axis=1)

    return matches


