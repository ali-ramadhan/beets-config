# !/usr/bin/python

# An album is a directory with no subdirectories. It must have a cover file.

import os
import sys
import glob

from PIL import Image
from rich.console import Console
from rich.progress import track

console = Console(highlight=False)

dir_to_walk = os.path.abspath(sys.argv[1])
verbose = True

# for root, dirs, files in track(os.walk(dir_to_walk), description="Walking through music"):
for root, dirs, files in os.walk(dir_to_walk):
    if len(dirs) > 0 and verbose:
        console.print(f"{root} is not an album as it contains subdirectories. Continuing.")
        continue
    else:
        n_mp3_files = len(glob.glob1(root, "*.mp3"))
        n_flac_files = len(glob.glob1(root, "*.flac"))
        
        if n_mp3_files + n_flac_files > 0:
            if verbose:
                console.print(f"{root} is an album with {n_mp3_files} mp3 files and {n_flac_files} flac files.")
            
            cover_files = glob.glob1(root, "cover*")
            if verbose:
                console.print(f"{root}: found {len(cover_files)} cover file(s): {cover_files}")

            if len(cover_files) == 0:
                console.print(f"[magenta]{root}[/magenta] contains [red]no covers[/red]!")

            if len(cover_files) > 1:
                console.print(f"[magenta]{root}[/magenta] contains [red]more than 1 cover[/red]: {cover_files}")
                
            for cover_file in cover_files:
                cover_filepath = os.path.join(root, cover_file)

                im = Image.open(cover_filepath)
                im_filesize = os.path.getsize(cover_filepath)

                if verbose:
                    print(f"{cover_filepath} image size: {im.size}, file size: {im_filesize} bytes")
                
                if im_filesize > 1024**2:  # if larger than 1 MiB
                    console.print(f"[magenta]{cover_filepath}[/magenta] is quite large at [red]{im_filesize / 1024**2:.2f} MiB[/red] and {im.size} pixels.")
                   
                if (im.size[0] < 600 or im.size[1] < 600) and verbose:
                    console.print(f"[magenta]{cover_filepath}[/magenta] is quite small at [blue]{im.size}[/blue] pixels and {im_filesize / 1024:.2f} KiB.")
        else:
            if verbose:
                console.print(f"{root} is not an album as it contains no mp3 or flac files..")
            continue

