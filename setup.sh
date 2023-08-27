#!/bin/sh

# python env
python -m venv klub-env
. klub-env/bin/activate

# pip
python -m pip install --upgrade pip

# packages
python -m pip install numpy pandas youtube_dl
python -m pip install xlrd

# ffmpeg
sudo apt update
sudo apt install ffmpeg

# deactivate environment
deactivate

