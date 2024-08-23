import pandas as pd
import os 

def download(name, link, outfile):
    import subprocess
    
    print('Downloading', name, 'from', link + '...')
    process = subprocess.Popen(['youtube-dl',
                                '--extract-audio',
                                '--cookies', './cookies.txt',
                                '--no-check-certificate',
                                '--audio-format', 'wav',
                                '-o', outfile, link],
                               stdout=subprocess.PIPE,
                               stderr=subprocess.PIPE)
    
    _, err = process.communicate()
    
    if err != b'':
        import sys
        print('Error downloading', name, 'from', link, file=sys.stderr)
        print(err.decode('utf-8'), file=sys.stderr)

if __name__ == "__main__":
    #df = pd.read_excel('Kærlighed10024/love10024.xlsx')
    #for i in range(0,101):
        #check if song exist
     #   if not os.path.exists('Kærlighed10024/' + str(i+1) + '.wav'):
      #      download(df['Sang - Kunstner'][i+1], df['link'][i], 'Kærlighed10024/' + str(i) + '.wav')
    download("test", "https://www.youtube.com/watch?v=pUROT2f6azM", '31.wav')