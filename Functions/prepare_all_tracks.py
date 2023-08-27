#!/usr/bin/env python3
import argparse
import multiprocessing
import os
import csv
import subprocess

err = subprocess.Popen(['pip', 'install', 'ffmpeg'], 
                       stdout=subprocess.DEVNULL, 
                       stderr=subprocess.PIPE).communicate()[1]

if len(err) != 0:
    print(err)
    exit(1)

def prepare_all_tracks(club_name = "klub.csv", input = None, output = None, t = -14, f = 3, length = 60):
    """
    Prepares all tracks in a folder
    ---------------------------------------
    club_name = path to csv with track information, the third column must have the start time in second from which to trim
    input = input folder with the tracks
    output = output folder to put the prepared tracks in
    t = Target volume in LUFS (-70 to -5)
    f = fade duration in seconds
    """
    
    # parser = argparse.ArgumentParser()
    # parser.add_argument('-input', type=str, default=os.path.join(os.path.curdir, 'tracks'), help='Input folder')
    # parser.add_argument('-output', type=str, default=os.path.join(os.path.curdir, 'prepared_tracks'),
    #                     help='Output folder')
    # parser.add_argument('-t', type=int, default=-14, help='Target volume in LUFS (-70 to -5)')
    # parser.add_argument('-f', type=float, default=3, help='Fade duration (seconds)')
    
    # args = parser.parse_args()
    ss_index = 2

    input = os.path.join(os.path.curdir, 'tracks') if input is None else input
    output = os.path.join(os.path.curdir, 'prepared_tracks') if output is None else output

    from prepare_track import prepare_track
    
    if not os.path.exists(input):
        exit(1)
    
    if not os.path.exists(output):
        os.mkdir(output)
    
    with multiprocessing.Pool() as p:
        with open(club_name, 'rt') as csvfile:
            reader = csv.reader(csvfile, delimiter=',', quotechar='"')
            
            for i, row in enumerate(reader, 1):
                
                infile = os.path.join(input, str(i) + '.wav')
                outfile = os.path.join(output, str(i) + '.wav')
                
                if not os.path.exists(infile):
                    continue
                
                p.apply_async(prepare_track, (infile, outfile, row[2], t, f, length))
        
        p.close()
        p.join()
