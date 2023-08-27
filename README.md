Er du også træt af at høre den samme klub 100 igen og igen hver fredag inden du tager i kb? Er din KABS også latterligt langsom til at klistre lydklip sammen i Audacity?

Alle disse problemer og mange flere er nu fortid - saml jeres yndlings YouTube/SoundCloud links i en .csv fil (Google Sheet -> export to csv), og producér en studio quality klub 100 på ~10 minutter.

Brugt til at samle  ./shoutouts/ og klub.csv brugt til denne klub 2^7 medfølger i dette repo.

Eksempler på brug af denne kan ses i mappen Examples, hvor csv og shoutouts kan findes:
* Klub 2^7 18': https://soundcloud.com/kenny-olsen/smkid-klub-2-7 af S/M+KID studiestarten '18.
* Klub 2^7 19': https://soundcloud.com/luke-leindance/smkid-klub27-2019 af S/M+KID studiestarten '19.
* KLub 4^4: https://soundcloud.com/luke-leindance/klub-44 af S/M+KID studiestarten '19.

OBS. de to Klub 2^7 samt 4^4 er lavet med en anden mappe struktur og vil derfor kræve en anden strukturering, se evt. https://github.com/falkaer/klub-100-maker.

<!-- # Hvordan, hvor og hvorfor gør jeg ting?

Før du kører noget som helst, bør indholdet af denne mappe have følgende struktur:

```
klub-100-maker/
├── shoutouts/
│   ├── 1.wav
│   ├── 2.wav
│   ├── ...
│   └── n.wav
├── klub.csv
├── dl.py
├── prepare_shoutout.py
├── prepare_track.py
├── prepare_all_shoutouts.py
├── prepare_all_tracks.py
└── combine.py
```

hvor ./shoutouts/n.wav indeholder skud ud'et til den n'te sang i klub 100en, hvis det giver mening. Skud ud'et kommer *før* sangen, så ./shoutouts/1.wav er jeres intro-skud-ud.

## klub.csv

Denne .csv fil indeholder information om sangene i en klub 100. Hver række svarer til en sang og et skud ud, hvor første kolonne er sangens navn, anden kolonne er et YouTube/SoundCloud link, og tredje kolonne er det timestamp (i sekunder) i sangen, hvor jeres ene minut af sangen skal begynde. -->

# Forarbejde
For at kunne lave en klub 100, skal der udfyldes et sheet med hvilke sange man ønsker, samt evt hvilke shoutouts man vil have.

Opbygningen af klub 100 foregår vha. sheet_templaten.

Det er vigtigt at kolonner har de samme navne, som angivet nedenunder.

## Sange
Arket “Sange” indeholder de sange som Klub 100 skal bestå af. 

I feltet ”Sang - Kunstner” skal en title samt kunster angives i formatter “sang - kunstner”. 

I feltet “link” angives et link til den ønskede sang, her skal angives et link (sider der understøttet ses her: https://github.com/ytdl-org/youtube-dl/blob/master/docs/supportedsites.md).

I feltet “starttidspunkt (i sek)” angives det antal sekunder inde i klippet at sangen skal startes, der vil herfra blive klippet 60 sekunder ud, som anvendes i Børne Klub 100.

Ønsker man at en sang skal have et bestemt shoutout inden sangen afspilles, skrives shoutsoutets titel i feltet “Shoutout”. Det er nemmest at kalde dine shoutouts tallene 1-100 i den rækkefølge de skal afspilles.

Det er muligt selv at tilføje flere kolonner med ting, som fx en kommentar. Disse vil blive ignoreret i bygningen af klub 100.

## Shoutouts
Arket “Shoutouts” indeholder de citater, som placeres mellem sangene.

I feltet “Shoutout titel” gives en titel som indikere hvad der siges/er essencen af shoutoutet. Dette vil blive shoutoutets reference og lydoptagelsen skal have dette navn for at blive matchet med den rette sang. Denne kolonne er den eneste nødvendige, hvis man selv indspiller shoutouts.

I feltet “link” angives et link til det ønskede citat. Dette bruges, hvis man ikke selv indspiller citater, men derimod henter dem fra et understøttet site (https://github.com/ytdl-org/youtube-dl/blob/master/docs/supportedsites.md).

I felterne “start tid (sek)” og “slut tid (sek)” angives start og sluttidspunktet i sekunder for det citat man ønsker. Disse tidspunkter referere til lyden i det angivne link.

I feltet “downloadet” angives med et “x” om det er et citat der skal downloades, da det ikke er fra et understøttet site (https://github.com/ytdl-org/youtube-dl/blob/master/docs/supportedsites.md).


# Kræver:
 * `python3`
 * `youtube-dl` - for at køre dl.py
 * `ffmpeg` - for at køre prepare_track.py, prepare_shoutout.py og combine.py


# Hvordan kører jeg det her?

For at kører scriptet skal du ligge inde i denne mappe og køre følgende kommandoer:

```bash
make install
python3 make_klub.py -c *mappe_lokation* -d *navn_på_csvfilen* -s *shoutout_type*
```

du kan specifere forskellige ting med følgende argumenter:

```bash
'-c', '--club_folder', default='Examples/Bums100', Det er lokationen af klub.csv og shoutouts
'-d', '--club_file', default='Nums100.xlsx', Det er navnet på klub.csv
'-o', '--output_name', default="Love100", Det er navnet på den output fil der bliver lavet
'-f', '--file_format', default="mp3", Det er filformatet på den output fil der bliver lavet
'-s', '--shoutout_type', default="none", Typen af shoutsouts der skal bruges. Kan være "none", "own" eller "links"
```
