import os
import random

# please update your music directory path
def play():
    try:
        music_dir = 'C:\\Users\\admin\\Music\\'
        songs = os.listdir(music_dir)
        song = random.choice(songs)
        os.startfile(os.path.join(music_dir, song))
    except:
        speak("Music files doesn't exists")
    
