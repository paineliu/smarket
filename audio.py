import os

class Audio:
    def play(self, filename):
        # print(filename)
        os.system("mplayer {} >/dev/null 2>&1".format(filename))
        # os.system("mplayer {}".format(filename))
