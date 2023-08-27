import pandas as pd

def get_template(name = "template", format = "xlsx", extra_song_cols = ["kommentar"], extra_shoutout_cols = ["kommentar"], sheet_types = ["Sange", "Shoutouts"]):
    """
    Downloades a sheet/csv to fill out for the club 100
    -----------------------------------------------------------
    name: the name of the downloaded file \n
    format: either xlsx or csv \n
    extra_song_cols: list of columns to add to the Sange sheet, choose from ["kommentar", "sluttidspunkt (i sek)"] \n
    extra_shoutout_cols: list of columns to add to the Sange sheet, choose from ["kommentar"] \n
    sheet_types: the csv/xlsx sheets to include, choose from ["Sange", "Shoutouts"]
    """
    song_cols = ["Sang - Kunstner", "link", "starttidspunkt (i sek)", "Shoutout"]
    shoutout_cols = ["Shoutout titel", "link", "starttidspunkt (i sek)", "sluttidspunkt (i sek)"] 

    songs = pd.read_excel("sheet_template.xlsx", sheet_name= "Sange", usecols = song_cols)
    shoutouts = pd.read_excel("sheet_template.xlsx", sheet_name= "Shoutouts", usecols= shoutout_cols)

    for extra in extra_song_cols:
        songs[extra] = []
    for extra in extra_shoutout_cols:
        shoutouts[extra] = []

    if format == "xlsx":
        with pd.ExcelWriter(name+".xlsx") as writer:
            if "Sange" in sheet_types:
                songs.to_excel(writer, sheet_name = "Sange", index = False, merge_cells = False)
            if "Shoutouts" in sheet_types:
                shoutouts.to_excel(writer, sheet_name = "Shoutouts", index = False, merge_cells = False)
    elif format == "csv":
        if "Sange" in sheet_types:
            songs.to_csv(name+"_songs.csv", index = False)
        if "Shoutouts" in sheet_types:
            shoutouts.to_csv(name+"_shoutouts.csv", index = False)

if __name__ == "__main__":
    get_template(format = "xlsx")