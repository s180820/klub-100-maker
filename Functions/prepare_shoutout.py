#!/usr/bin/env python3
import argparse
import os
import subprocess
import csv
import multiprocessing

err = subprocess.Popen(['pip', 'install', 'ffmpeg'], 
                       stdout=subprocess.DEVNULL, 
                       stderr=subprocess.PIPE).communicate()[1]

if len(err) != 0:
    print(err)
    exit(1)

def prepare_shoutout(input, output, t=-14, trim = False, ss = 0, length = 5):
    """
    Prepares a shoutout by normalising and more
    ---------------------------------------------
    input = The input file to prepare \n
    output = The output file name \n
    t = the target volume in LUFS (-70 to -5) \n
    trim = whether or not to trim the shoutout \n
    ss = the position to start the trim at \n
    length = the length of the shoutout
    """
    print('Preparing', input + '...')
    # trim
    if trim:
        p1 = subprocess.Popen(['ffmpeg',
                            '-loglevel', 'error',
                            '-ss', str(ss),
                            '-i', input, '-t', str(length), '-f', 'wav', '-'],
                            stdout=subprocess.PIPE)
        input = '-'
        
    # two-pass ebu r128 loudnorm filter
    # loudnorm pass 1
    p2 = subprocess.Popen(['ffmpeg', '-loglevel', 'error',
                        '-i', input,
                        '-pass', '1', '-af', 'loudnorm=I=' + str(t) + ':TP=-1',
                        '-f', 'wav', '-y', os.devnull],  # generate log in null
                        stdin=subprocess.PIPE,
                        stdout=subprocess.PIPE)
    
    # loudnorm pass 2
    p3 = subprocess.Popen(['ffmpeg', '-loglevel', 'error',
                        '-i', input,
                        '-pass', '2', '-af', 'loudnorm=I=' + str(t) + ':TP=-1',
                        '-f', 'wav', '-y', output],
                        stdin=subprocess.PIPE,
                        stdout=subprocess.PIPE)

    if trim:
        trimmed = p1.communicate()[0]
        p2.communicate(trimmed)
        p3.communicate(trimmed)[0]

    else:
        p2.communicate()
        p3.communicate()

def prepare_all_shoutouts(songs_csv, input = "shoutouts", output = "prepared_shoutouts", t = -14, trim_vals = None): 
    """
    Prepares all shoutouts
    -------------------------
    songs_csv = csv with the songs (used to find number of songs) \n
    input = input folder with shoutouts \n
    output = name of output folder \n
    t = Target volume in LUFS (-70 to -5) \n
    trim_vals = data frame with start time of SO as first column and length as second
    """

    # input = os.path.join(os.path.curdir, 'shoutouts') if input is None else input
    # output = os.path.join(os.path.curdir, 'prepared_shoutouts') if output is None else output
    
    if not os.path.exists(input):
        exit(1)
    
    if not os.path.exists(output):
        os.mkdir(output)

    trim = False if trim_vals is None else True
    with multiprocessing.Pool() as p:
        with open(songs_csv, 'rt') as csvfile:
            reader = csv.reader(csvfile, delimiter=',', quotechar='"')
            
            for i, row in enumerate(reader, 1):
                
                infile = os.path.join(input, str(i) + '.wav')
                outfile = os.path.join(output, str(i) + '.wav')
                
                if not os.path.exists(infile):
                    continue
                
                if trim:
                    p.apply_async(prepare_shoutout, (infile, outfile, t, trim, trim_vals.iloc[i-1,0], trim_vals.iloc[i-1,1]))
                else:
                    p.apply_async(prepare_shoutout, (infile, outfile, t, trim))
        
        p.close()
        p.join()

if __name__ == "__main__":
    from prepare_csv import create_shoutout_csv, create_song_csv
    from dl import download_all
    from prepare_shoutout import prepare_all_shoutouts
    from prepare_csv import get_trim_vals

    # create_shoutout_csv("so.xlsx")
    # create_song_csv("so.xlsx", csv_name = "song_test.csv")
    # download_all(dl_path="sos", csv_name="Shoutouts.csv")
    trim_vals = get_trim_vals()
    prepare_all_shoutouts(input = "sos", output = "sos_prep", trim_vals = trim_vals, songs_csv = "song_test.csv")