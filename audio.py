import os

class Audio:
    def play(self, filename):
        os.system("mplayer {}".format(filename))

