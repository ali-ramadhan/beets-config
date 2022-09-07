# !/usr/bin/python

# An album is a directory with no subdirectories. It must have a cover file.

import os
import sys
import glob
import hashlib

from PIL import Image
from rich.console import Console
from rich.progress import track
from mutagen.flac import FLAC
from mutagen.mp3 import MP3

console = Console(highlight=False)

dir_to_walk = os.path.abspath(sys.argv[1])

verbose = False

# for root, dirs, files in track(os.walk(dir_to_walk), description="Walking through music"):
for root, dirs, files in os.walk(dir_to_walk):
    mp3_files = glob.glob1(root, "*.mp3")
    flac_files = glob.glob1(root, "*.flac")

    n_mp3_files = len(mp3_files)
    n_flac_files = len(flac_files)
    
    if n_mp3_files + n_flac_files == 0:
        if verbose:
            console.print(f"{root} is not an album as it contains no mp3 or flac files..")
        continue
    else:
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

            cover_filesize_large = im_filesize > 1.5 * 1024**2
            cover_dims_small = (im.size[0] < 500 or im.size[1] < 500)

            if cover_filesize_large:
                console.print(f"[magenta]{cover_filepath}[/magenta] image size: [cyan]{im.size} pixels[/cyan], file size: [red]{im_filesize / 1024:.2f} KiB[/red]")
            elif cover_dims_small:
                console.print(f"[magenta]{cover_filepath}[/magenta] image size: [blue]{im.size} pixels[/blue], file size: [cyan]{im_filesize / 1024:.2f} KiB[/cyan]")
            else:
                console.print(f"[magenta]{cover_filepath}[/magenta] image size: [cyan]{im.size} pixels[/cyan], file size: [cyan]{im_filesize / 1024:.2f} KiB[/cyan]")

            with open(cover_filepath, "rb") as cf:
                bytes = cf.read() # read entire file as bytes
                cover_sha256 = hashlib.sha256(bytes).hexdigest()

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
                    if verbose:
                        console.print(f"[magenta]{flac_filepath}[/magenta]: [green]cover sha256 match[/green]")
                else:
                    pic = flac.pictures[0]
                    console.print(f"[magenta]{flac_filepath}[/magenta]: [red]cover sha256 do not match[/red] ({pic.width}x{pic.height}, {len(pic.data) / 1024:.2f} KiB)")
