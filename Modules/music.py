import os
import random


def play():
    music_dir = 'C:\\Users\\admin\\Music\\'
    songs = os.listdir(music_dir)
    song = random.choice(songs)
    os.startfile(os.path.join(music_dir, song))
