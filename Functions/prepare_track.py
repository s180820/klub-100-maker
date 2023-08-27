#!/usr/bin/env python3
import argparse
import os
import subprocess
import multiprocessing
import csv
import pandas as pd

err = subprocess.Popen(['pip', 'install', 'ffmpeg'], 
                       stdout=subprocess.DEVNULL, 
                       stderr=subprocess.PIPE).communicate()[1]

if len(err) != 0:
    print(err)
    exit(1)

def prepare_track(input, output, ss=0, t=-14, f=3, length = 60):
    """
    Prepares a track by normalising, fading and more
    ---------------------------------------------
    input = The input file to prepare
    output = The output file name
    ss = the position to start the trim at
    t = the target volume in LUFS (-70 to -5)
    f = the number of seconds to fade
    length = the length of the track to use
    """
    print('Preparing', input + '...')
    
    # trim
    p1 = subprocess.Popen(['ffmpeg',
                           '-loglevel', 'error',
                           '-ss', str(ss),
                           '-i', input, '-t', str(length), '-f', 'wav', '-'],
                          stdout=subprocess.PIPE)
    
    # normalize
    # two-pass ebu r128 loudnorm filter
    # loudnorm pass 1
    p2 = subprocess.Popen(['ffmpeg',
                           '-loglevel', 'error',
                           '-i', '-',
                           '-pass', '1', '-af', 'loudnorm=I=' + str(t) + ':TP=-1',
                           '-f', 'wav', '-y', os.devnull],  # generate log but no other output
                          stdin=subprocess.PIPE,
                          stdout=subprocess.PIPE)
    
    # loudnorm pass 2
    p3 = subprocess.Popen(['ffmpeg',
                           '-loglevel', 'error',
                           '-i', '-',
                           '-pass', '2', '-af', 'loudnorm=I=' + str(t) + ':TP=-1',
                           '-f', 'wav', '-'
                           ],
                          stdin=subprocess.PIPE,
                          stdout=subprocess.PIPE)
    
    # fade
    p4 = subprocess.Popen(['ffmpeg',
                           '-loglevel', 'error',
                           '-i', '-', '-af',
                           'afade=t=in:ss=0:d=' + str(f) +
                           ',afade=t=out:st=' + str(length - f) + ':d=' + str(f),
                           '-f', 'wav', '-y', output],
                          stdin=subprocess.PIPE,
                          stdout=subprocess.PIPE)
    
    trimmed = p1.communicate()[0]
    
    p2.communicate(trimmed)
    normalized = p3.communicate(trimmed)[0]
    
    return p4.communicate(normalized)[0] # return stdout in case output is '-'

def prepare_all_tracks(songs_csv = "klub.csv", input = "tracks", output = "prepared_tracks", t = -14, f = 3, length = 60):
    """
    Prepares all tracks in a folder
    ---------------------------------------
    song_csv = path to csv with track information, the third column must have the start time in second from which to trim
    input = input folder with the tracks
    output = output folder to put the prepared tracks in
    t = Target volume in LUFS (-70 to -5)
    f = fade duration in seconds
    length = length of song, if specified as a pd data frame with start time as first column and length as second, this will be used 
    """
    
    ss_index = 2

    # input = os.path.join(os.path.curdir, 'tracks') if input is None else input
    # output = os.path.join(os.path.curdir, 'prepared_tracks') if output is None else output

    
    if not os.path.exists(input):
        exit(1)
    
    if not os.path.exists(output):
        os.mkdir(output)
    
    with multiprocessing.Pool() as p:
        with open(songs_csv, 'rt') as csvfile:
            reader = csv.reader(csvfile, delimiter=',', quotechar='"')
            
            for i, row in enumerate(reader, 1):
                
                infile = os.path.join(input, str(i) + '.wav')
                outfile = os.path.join(output, str(i) + '.wav')
                
                if not os.path.exists(infile):
                    continue
                
                if isinstance(length, pd.DataFrame):
                    p.apply_async(prepare_track, (infile, outfile, length.iloc[i-1,0], t, f, length.iloc[i-1,1]))
                else:
                    p.apply_async(prepare_track, (infile, outfile, row[2], t, f, length))
        
        p.close()
        p.join()
