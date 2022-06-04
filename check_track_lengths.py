# !/usr/bin/python

import os
import sys
import glob
import librosa
import eyed3

from rich.console import Console
from rich.progress import track
from tinytag import TinyTag
from soundfile import SoundFile
from mutagen.flac import FLAC

console = Console(highlight=False)

dir_to_walk = os.path.abspath(sys.argv[1])
verbose = False

for root, dirs, files in os.walk(dir_to_walk):
    mp3_files = glob.glob1(root, "*.mp3")
    flac_files = glob.glob1(root, "*.flac")
    
    for mp3_file in mp3_files:
        mp3_filepath = os.path.join(root, mp3_file)
        
        track_length_librosa = librosa.get_duration(filename=mp3_filepath)
        track_length_eyed3 = eyed3.load(mp3_filepath).info.time_secs
        track_length_tinytag = TinyTag.get(mp3_filepath).duration
        
        track_lengths = [track_length_librosa, track_length_eyed3, track_length_tinytag]
        delta = max(track_lengths) - min(track_lengths)
        
        color = "green" if delta < 1 else "red"
        console.print(f"[magenta]{mp3_filepath}[/magenta] track length: librosa={track_length_librosa}, eyed3={track_length_eyed3}, tinytag={track_length_tinytag}, [{color}]delta={delta}[/{color}]")
        
    for flac_file in flac_files:
        flac_filepath = os.path.join(root, flac_file)
        
        track_length_librosa = librosa.get_duration(filename=flac_filepath)
        track_length_tinytag = TinyTag.get(flac_filepath).duration
        
        sf = SoundFile(flac_filepath)
        track_length_soundfile = sf.frames / sf.samplerate
        
        
        
        track_lengths = [track_length_librosa, track_length_tinytag, track_length_soundfile]
        delta = max(track_lengths) - min(track_lengths)
        
        color = "green" if delta < 1 else "red"
        console.print(f"[magenta]{flac_filepath}[/magenta] track length: librosa={track_length_librosa}, tinytag={track_length_tinytag}, soundfile={track_length_soundfile}, [{color}]delta={delta}[/{color}]")

