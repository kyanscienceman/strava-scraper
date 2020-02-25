import pandas as pd
import numpy as numpy
import jellyfish

### NOTE: We should decide how we want to format the manually link files so they are eay to unpack and use on dfs. As of right now, the marathon and strava csvs are formatted in different ways. Marathon data is by individual race and strava data is by marathon location and contains data from multiple years. We will have to decide if we want to split up the strava data and index matches based on those smaller dataframes or if we should combine marathon data into one larger index 

### Additionally: I have named this file chicago_linking, but it most likely can be used for linking any marathon considering we format all of our scrapes the same way

def create_marathon_df(filename, raceID):
    '''
    Takes in the csv file of a race's results scraped from the marathon website and turns it into a useable dataframe object

    Inputs:
        filename (string) name of the file we want to turn into a df
    Returns:
        marathon_df (DataFrame) 
    '''

    marathon_df = pd.read_csv(filename, header=None) #read without a header because the first row of csv contains real data
    marathon_df.columns = ['Name', 'Gender_and_Age', 'Time']
    marathon_df['Gender'] = marathon_df.gender_and_age.str[0]
    marathon_df['Age'] = marathon_df.gender_and_age.str[1:]
    marathon_df = marathon_df.drop['Gender_and_Age']
    marathon_df['RaceID'] = raceID
    cols = ['RaceID', 'Name', 'Gender', 'Age']

    return marathon_df

def create_strava_df(filename):
    '''
    Takes in the csv file of a race's results scraped from strava and turns it into a useable dataframe object. No processing needed here. This helper function was written for consistency purposes

    Inputs:
        filename (string) name of the file we want to turn into a df
    Returns:
        strava_df (DataFrame) 
    '''

    strava_df = pd.read_csv(filename, sep='|')

    return strava_df

def create_matches_df(links_filename, marathon_df, strava_df):
    '''
    Uses a csv of indexes of known links to build a matches df. csv is in format marathon_index, strava_index

    Inputs:
        links_filename (string) name of csv file with indexes of matches
        marathon_df (DataFrame)
        strava_df (DataFrame)
    Returns:
        matches (DataFrame)
    '''

    matches = pd.read_csv(links_filename)
    matches.columns = ['marathon_index', 'strava_index']

    matches = matches.merge(marathon_df, left_on='marathon_index', right_on='index_num') #might have to change to 'right_on='index''
    matches = matches.merge(strava_df, left_on='strava_index', right_on='index_num') #might have to change to 'right_on='index''
    matches = matches.drop(columns=['marathon_index', 'strava_index'])

    matches.columns = ['RaceID_m', 'Name_m', 'Gender_m', 'Age_m', 'RaceID_s', 'Name_s', 'Gender_s', 'Age_s', 'Time1_s', 'Time2_s', 'Shoes_s']

    return matches



