import pandas as pd
import numpy as numpy
import jellyfish

### NOTE: I have named this file chicago_linking, but it most likely can be used for linking any marathon considering we format all of our scrapes the same way

### NOTE: We should think about actually just combining into one df despite the computational intensity. As it is right now, this function is going to end with us returning a variable number of dataframes depending on the amount of unique entries in the raceID column (read: how many races we're tracking per location). We could prevent this by instead combining by race and just blocking on identical raceID, similar to how we block on city in pa4. This reduces computational intensity and allows us to have one set of matches/unmatches/possible dfs per race location

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

def create_strava_df_list(filename):
    '''
    Takes in the csv file of a race's results scraped from strava and turns it into a list of useable dataframe objects, separated by race year.

    Inputs:
        filename (string) name of the file we want to turn into a df
    Returns:
        strava_df_list (list) list of DataFrame objects 
    '''

    master_strava_df = pd.read_csv(filename, sep='|')

    strava_df_list = [] 
    for race in df.raceID.unique():
        new_df = master_strava_df[master_strava_df['raceID'] == race]
        strava_df_list.append(new_df)

    return strava_df_list

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

def create_unmatches_df(marathon_df, strava_df):
    '''
    Takes both dfs and creates a df of unmatches by randomly pairing indexes

    Inputs:
        marathon_df (DataFrame)
        strava_df (DataFrame)
    Returns:
        unmatches (DataFrame)
    '''

    ms = marathon_df.sample(1000, replace=True, random_state= 1234)
    ss = strava_df.sample(1000, replace=True, random_state= 5678)
    ms = ms.reset_index()
    ss = ss.reset_index()

    unmatches = pd.concat([ms, ss], aaxis =1)
    unmatches = unmatches.drop(columns=['index_num']) #make sure this is the actual name for the index column
    unmatches.columns = ['RaceID_m', 'Name_m', 'Gender_m', 'Age_m', 'RaceID_s', 'Name_s', 'Gender_s', 'Age_s', 'Time1_s', 'Time2_s', 'Shoes_s'] #Ensure that the columns actually end up in this order

def create_tuple_sets(mu, lambda_):
    '''
    Combine previous functions and use them to determine a set of tuples that will be used to determine if a row is a match
    '''


