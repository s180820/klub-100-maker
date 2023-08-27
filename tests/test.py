from Functions.dl import download, download_all
from Functions.prepare_track import prepare_all_tracks
from Functions.prepare_csv import create_song_csv
from Functions.combine import combine
from Functions.prepare_shoutout import prepare_shoutout


# download("Disney intro", "https://www.youtube.com/watch?v=Bfp4zusaQ5g", "disneyintro.wav")

# prepare_track("disneyintro.wav", "disneyintro2.wav", ss=0, t=-14, f=3, length = 60)

if __name__ == "__main__":
    # create_song_csv("Examples/Børne Klub 100/Børne Klub 100.xlsx", csv_name = "Songs.csv", n_songs=4)
    # download_all(csv_name="Songs.csv")
    # prepare_all_tracks(n_songs = 5, input = None, output = None, t = -14, f = 3, length = 60)
    #combine(club_name = "Songs.csv", prep_shoutout_path = None, prep_tracks_path = None, output_name = None, fileformat = "mp3", with_shoutouts = False)
    download("bamse", "https://www.youtube.com/watch?v=4Z5f25b48ng", "bamse.wav")
    prepare_shoutout(input = "bamse.wav", output = "test.wav", trim = True, ss = 154, length = 5)