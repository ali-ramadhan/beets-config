# !/usr/bin/python

# An album is a directory with no subdirectories. It must have a cover file.

import os
import sys
import glob
from PIL import Image

dir_to_walk = os.path.abspath(sys.argv[1])

for root, dirs, files in os.walk(dir_to_walk):
    if len(dirs) > 0:
        print(f"{root} is not an album.")
        continue
    else:
        n_mp3_files = len(glob.glob1(root, "*.mp3"))
        n_flac_files = len(glob.glob1(root, "*.flac"))
        
        if n_mp3_files + n_flac_files > 0:
            print(f"{root} is an album with {n_mp3_files} mp3 files and {n_flac_files} flac files.")
            
            cover_files = glob.glob1(root, "cover*")
            print(f"{root}: found {len(cover_files)} cover files: {cover_files}")

            cover_filepath = os.path.join(root, cover_files[0])
            im = Image.open(cover_filepath)
            print(f"cover image size: {im.size}, file size: {os.path.getsize(cover_filepath)} bytes")
        else:
            printf(f"{root} is not an album.")
            continue

