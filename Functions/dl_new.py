import yt_dlp
import pandas as pd
import glob
import os

class MyLogger:
    def debug(self, msg):
        # For compatibility with youtube-dl, both debug and info are passed into debug
        # You can distinguish them by the prefix '[debug] '
        if msg.startswith('[debug] '):
            pass
        else:
            self.info(msg)

    def info(self, msg):
        pass

    def warning(self, msg):
        pass

    def error(self, msg):
        print(msg)

def my_hook(d):
        if d['status'] == 'finished':
            print('Done downloading, now post-processing ...')

def download_song(name, link, output_folder, output_format: str = 'wav'):

    ydl_opts = {
    'format': f'{output_format}/bestaudio/best',
    'postprocessors': [{  # Extract audio using ffmpeg
        'key': 'FFmpegExtractAudio',
        'preferredcodec': output_format,
    }],
    'logger': MyLogger(),
    'progress_hooks': [my_hook],
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        error_code = ydl.download([link])
    
    for file in glob.glob('*.wav'):
        os.rename(file, f'{name}.wav')
        #move the downloaded file to the correct folder
    os.rename(f'{name}.wav', f'{output_folder}/{name}.wav')

def download_all_songs(csv_name = 'Songs.csv', output_format: str = 'wav', output_folder = 'tracks'):
    df = pd.read_excel(csv_name)
    for i in range(len(df)):
        download_song(str(i+1), df['link'][i], output_folder, output_format)

if __name__ == "__main__":
    download_all_songs('Kærlighed10024/love10024.xlsx', 'wav', 'tracks')