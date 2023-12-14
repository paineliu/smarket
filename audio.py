import os

def play_sound(filename):
    os.system("mplayer {}".format(filename))

