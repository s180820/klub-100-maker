# script for preparing files for the club 100 maker

import pandas as pd
from pydub import AudioSegment
import os
import argparse
import random 

# prepare csv

songs = pd.read_csv("Sange og citater - sange.csv", usecols= [0, 1, 2, 3, 10])
songs = songs.loc[songs["Sang valgt"] == "X"]
songs = songs.sort_values(by = "0")
songs = songs.drop(["Sang valgt", "0"], axis = 1)

songs.to_csv("klub.csv", header = False, index = False)

# prepare shoutouts



formats_to_convert = ['.m4a']

for (dirpath, dirnames, filenames) in os.walk("Shoutouts/"):
    shoutout_names = [f.replace(".m4a", "") for f in filenames]
    #song_names = pd.read_csv("klub.csv", header = None)
    song_names = songs.iloc[:,0].values.tolist()
    song_ind = songs.iloc[:, ]

    #associated = [ind for ind, e in enumerate(song_names) if e in shoutout_names] #[i for i, e in enumerate(song_names) if e in set(shoutout_names)]
    associated = [str(i) for i in range(1,129)]
    associated = [int(i)-1 for i in associated if i in shoutout_names]
    # shout_indices = {}
    # for i, e in enumerate(song_names):
    #     shout_ind = [ind for ind, en in enumerate(shoutout_names) if e == en]
    #     print(shout_ind)
    #     #shout_indices[shout_ind[0]:i]

    # print(shout_ind)

    random_assignment = [i for i in range(128) if i not in associated]

    print(associated, random_assignment)

    assert set(associated) & set(random_assignment) == set()

    for index, filename in enumerate(filenames):
        if filename.endswith(tuple(formats_to_convert)):
            
            if index in associated:
                shoutout_name = filename
            else:
                shoutout_name = random.choice(random_assignment)
                random_assignment.remove(shoutout_name)


            filepath = dirpath + '/' + filename
            (path, file_extension) = os.path.splitext(filepath)
            file_extension_final = file_extension.replace('.', '')
            #try:
            track = AudioSegment.from_file(filepath,
                    file_extension_final)
            #wav_filename = filename.replace(file_extension_final, 'wav')
            #wav_path = dirpath + '/' + wav_filename
            wav_path = "Shoutouts/" + str(shoutout_name+1) +".wav"
            print('CONVERTING: ' + str(filepath))
            file_handle = track.export(wav_path, format='wav')
            os.remove(filepath)
            #except:
             #   print("ERROR CONVERTING " + str(filepath))





