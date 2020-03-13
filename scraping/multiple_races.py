import pandas as pd
import numpy as np
import jellyfish
import matches

def find_consistent_runners(acceptable_name_score=0.85):
    '''
    Takes in the list of matched runners and produces a list of people who ran multiple races

    Inputs:
        None (only uses the matches dataframe)
    Returns:
        consistent_runners (DataFrame) the df of runners who have ran multiple races
    '''

    matches = pd.read_csv('race_result/master_matches.csv')
    matches_indexes = []

    for p_index, p_row in matches.iterrows():
        primary_time = p_row.at['Time']
        primary_name = p_row.at['Name']
        primary_gender = p_row.at['Gender']
        primary_age_lower = p_row.at['Age_Lower']
        primary_age_upper = p_row.at['Age_Upper']
        primary_raceid = p_row.at['RaceID']

        searchable_matches = matches[
            (matches['RaceID'] != primary_raceid) & 
            (matches['Gender'] == primary_gender) & 
            (matches['Time'] <= primary_time + 1200) & 
            (matches['Time'] >= primary_time - 1200) &
            (matches['Age_Lower'] <= primary_age_upper)]

        # (matches['Age_Upper'] <= primary_age_upper) <- want to add this as well but I don't know how to do & for all those tuples and either or of the last two stipulations

        print(p_index)

        for s_index, s_row in searchable_matches.iterrows():
            secondary_name = s_row.at['Name']

            name_score = jellyfish.jaro_winkler(primary_name, secondary_name)

            if name_score >= acceptable_name_score:
                matches_indexes = []

    consistent_runners = matches[matches_indexes]

    return consistent_runners

def return_runners_of_multiple_races(df):
	df = df[df.groupby("Name")["Name"].transform("size") > 1]
	df = df.sort_values(by="Name")
	return df


'''

def return_all_races_one_runs(name):
	RACE_DICT = matches.RACE_DICT
	personal_df = pd.DataFrame()
	for official_csv,_ in RACE_DICT.values():
		df = pd.read_csv('race_result/' + official_csv, header=None)
		personal_df.append(df[df[0] == name])
		print(df[0])
		print(official_csv, personal_df)
	return personal_df
'''