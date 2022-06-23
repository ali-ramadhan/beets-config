# !/usr/bin/python

import os
import sys
import glob
import shutil
import subprocess

from rich.console import Console

console = Console(highlight=False)

lame_bitrate_arg = {"320": "-b 320", "V0": "-V 0"}

dirs_to_transcode = map(os.path.abspath, sys.argv[1:])

for dir_to_transcode in dirs_to_transcode:
    for bitrate in ("320", "V0"):
        dir_dst = os.path.join(os.path.dirname(dir_to_transcode), os.path.basename(dir_to_transcode).replace("FLAC", f"MP3 {bitrate}"))
        console.print(f"[bold]Copying[/bold]: [magenta]{dir_to_transcode}[/magenta] -> [dark_orange]{dir_dst}[/dark_orange]")
        shutil.copytree(dir_to_transcode, dir_dst)
        
        for root, dirs, files in os.walk(dir_dst):
            flac_filenames = glob.glob1(root, "*.flac")
            
            for flac_filename in flac_filenames:
                flac_filepath = os.path.join(root, flac_filename)
                proc = subprocess.run(["flac", "-t", f"{flac_filepath}"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
                
                if proc.returncode == 0:
                    console.print(f"[bold]Testing[/bold]: [magenta]{flac_filepath}[/magenta] [green]OK[/green]")
                else:
                    console.print(f"[bold]Testing[/bold]: [magenta]{flac_filepath}[/magenta] [red]BAD[/red]")
                
                mp3_filepath = flac_filepath.replace(".flac", ".mp3")
                # cmd_lame = f"flac -dc {flac_filepath} | lame {lame_bitrate_arg[bitrate]} - {mp3_filepath}"
                # print(cmd_lame)
                # proc = subprocess.run(cmd_lame, shell=True)
                
                ps = subprocess.Popen(["flac", "-dc", f"{flac_filepath}"], stdout=subprocess.PIPE, stderr=subprocess.DEVNULL)
                ps2 = subprocess.Popen(["lame", f"{lame_bitrate_arg[bitrate]}", "-", f"{mp3_filepath}"], stdin=ps.stdout)
                ps.wait()
                
                if ps.returncode == 0:
                    console.print(f"[bold]Transcoding[/bold]: [dark_orange]{mp3_filepath}[/dark_orange] [green]OK[/green]")
                else:
                    console.print(f"[bold]Transcoding[/bold]: [dark_orange]{mp3_filepath}[/dark_orange] [red]BAD[/red]")
                    
                os.remove(flac_filepath)
                    
