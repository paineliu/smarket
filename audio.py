import os

class Audio:
    def play(self, filename):
        os.system("mplayer {} >/dev/null 2>&1".format(filename))

