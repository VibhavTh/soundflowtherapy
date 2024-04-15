import csv
import pandas
import os
import sys
import random

def getPlaylistSongs(userMood) -> list:
    # Getting the Track URIs
    dir = cwd = os.getcwd()
    dataset = pandas.read_csv(dir + "/vibhavhelper/data/tracksInSpotify.csv")
    dataset = pandas.Series.tolist(dataset)
            
    # Initialize empty lists to store tracks and reformatted data
    trackURIs = []
    trackMood = []
    formatted_track_URIs = []

        
    # Iterate over each anelement in the dataset
    for elem in dataset:
        # Strip brackets and single quotes, then split by comma and space to get individual items
        res = elem[0].strip('][').replace("'", "").split(', ')
        trackURIs.append(res[0])  # Append the reformatted data to the data list
        trackMood.append(res[1])  # Append the track name to the tracks list
    for i, mood in enumerate(trackMood):
        #check if mood is sad
        if mood == userMood:
            spotify_uri = f"spotify:track:{trackURIs[i]}"
            # Add the formatted URI to the new list
            formatted_track_URIs.append(spotify_uri)
                
    # Randomly chooses 10 songs from the new formatted list to create final form of the playlist to use in main.py      
    random_formatted_track_URIs = random.sample(formatted_track_URIs, k= min(len(formatted_track_URIs),10))
    return random_formatted_track_URIs