#from genericpath import isdir
import os
import random
import subprocess
from re import sub
#from tkinter.messagebox import askokcancel
import tkinter as tk
from tkinter import filedialog
from time import sleep


# >> random playlist maker <<
# chooses files from a folder containing audio files,
# creates an .m3u playlist with their paths.

# take input number from Entry
def printtext():
    global number
    string = number.get() 
    print(string)
    root.destroy()


# tkinter root window
root = tk.Tk()

number = tk.Entry(root)
number.pack()
number.focus_set()

b = tk.Button(root,text='okay',command=printtext)
b.pack(side='bottom')
root.mainloop()

# ask where the main music folder is:
mainFolder = filedialog.askdirectory(title='Choose a folder:')
currentPath = mainFolder

# TO DO:
# prevent repeated songs
# choose number of songs
# and/or choose by total duration (e.g. make a 30-minute playlist)


# removing hidden files
def rmvHidden(list):
    for f in list:
        if f.startswith('.'):
            list.remove(f)
    return list                

# check if there are sounds in the folder, make a list of them

def theresSounds(folder):
    songs = []
    for f in rmvHidden(os.listdir(folder)):
        if (f.endswith('.wav') or f.endswith('.mp3') or f.endswith('.flac') or f.endswith('.m4a') or f.endswith('.ape')):
            songs.append(os.path.join(folder, f))
    if len(songs) > 0:
        return songs
    else:
        return 0    

# check if there are folders inside the current folder, list them

def theresFolders(folder):
    subfolders = []
    for f in rmvHidden(os.listdir(folder)):
        if os.path.isdir(os.path.join(folder, f)):
            subfolders.append(os.path.join(folder, f))
    if len(subfolders) > 0:
        return subfolders
    else:
        return 0            


# main song finder

def songFinderCore(folder):
    if theresSounds(folder):
        # found some audio, let's choose one file
        snd = random.choice(theresSounds(folder))
        return snd
    elif theresFolders(folder):
        # no audio here, but there are folders. Let's check them
        fldr = random.choice(theresFolders(folder))
        currentPath = fldr
        return songFinderCore(fldr)
    else:
        # can't find audio anywhere. Go back to the main folder and start again
        currentPath = mainFolder;
        return songFinderCore(mainFolder)  


# final playlist
musicas = []

# number of tracks
while len(musicas) < 10:
    mus = songFinderCore(mainFolder)
    if mus not in musicas:  # should remove duplicates 
        musicas.append(mus)


# write an .m3u file with the playlist
with open('playlist.m3u', 'w') as playlist:
    for m in musicas:
        playlist.write(m + "\n")

# open and start playing music
os.system("open " + 'playlist.m3u')

# wait a bit and remove the .m3u file.
# for cleanliness
# If you like your playlist, you can save it via the music player
sleep(5)
os.remove('playlist.m3u')

