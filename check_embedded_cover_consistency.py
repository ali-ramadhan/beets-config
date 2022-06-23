# !/usr/bin/python

import os
import sys
import glob
import hashlib

from rich.console import Console
from rich.progress import track

from mutagen.flac import FLAC
from mutagen.mp3 import MP3

console = Console(highlight=False)

dir_to_walk = os.path.abspath(sys.argv[1])
verbose = False

for root, dirs, files in os.walk(dir_to_walk):
    if len(dirs) > 0:
        if verbose:
            console.print(f"{root} is not an album as it contains subdirectories. Continuing.")
        continue
    else:
        cover_files = glob.glob1(root, "cover*")
        mp3_files = glob.glob1(root, "*.mp3")
        flac_files = glob.glob1(root, "*.flac")
        
        if len(cover_files) == 0:
            console.print(f"[magenta]{root}[/magenta] contains [red]no covers[/red]!")
            continue

        if len(cover_files) > 1:
            console.print(f"[magenta]{root}[/magenta] contains [red]more than 1 cover[/red]: {cover_files}")
            continue
        
        cover_filepath = os.path.join(root, cover_files[0])
        with open(cover_filepath, "rb") as cf:
            bytes = cf.read() # read entire file as bytes
            cover_sha256 = hashlib.sha256(bytes).hexdigest();
        
        for flac_file in flac_files:
            flac_filepath = os.path.join(root, flac_file)
            flac = FLAC(flac_filepath)
            
            if len(flac.pictures) == 0:
                console.print(f"[magenta]{flac_filepath}[/magenta] contains [red]no covers[/red]!")
                continue
            
            if len(flac.pictures) > 1:
                console.print(f"[magenta]{flac_filepath}[/magenta] contains [red]more than 1 cover[/red]!")
                continue
            
            flac_cover_sha256 = hashlib.sha256(flac.pictures[0].data).hexdigest()
            
            if flac_cover_sha256 == cover_sha256:
                console.print(f"[magenta]{flac_filepath}[/magenta]: [green]cover sha256 match[/green]")
            else:
                console.print(f"[magenta]{flac_filepath}[/magenta]: [red]cover sha256 do not match[/red]")
                
        for mp3_file in mp3_files:
            mp3_filepath = os.path.join(root, mp3_file)
            mp3 = MP3(mp3_filepath)
            
            mp3_cover_sha256 = hashlib.sha256(mp3.tags['APIC:'].data).hexdigest()
            
            if mp3_cover_sha256 == cover_sha256:
                console.print(f"[magenta]{mp3_filepath}[/magenta]: [green]cover sha256 match[/green]")
            else:
                console.print(f"[magenta]{mp3_filepath}[/magenta]: [red]cover sha256 do not match[/red]")

