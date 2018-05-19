import subprocess
import os
import random

# Globals
AUDIO_FILES_DIRECTORY = "./music/"

BROADCAST_FREQUENCY = "93.8"

def main():
    # Do stuff
    build_playlist()
    play_playlist()


def build_playlist():
    files = os.listdir(AUDIO_FILES_DIRECTORY)
    random.shuffle(files)

    with open("playlist.m3u", "w") as file:
        for filename in files:
            # Skip comments
            if filename.startswith('#'):
                continue
            else:
                file.write(AUDIO_FILES_DIRECTORY + filename + "\n")


def play_playlist():
    print("Playing playlist on frequency " + BROADCAST_FREQUENCY)

    #ps = subprocess.Popen(["ffmpeg", "-nostdin", "-i", file, "-f", "s16le", "-ar", "22.05k", "-ac", "1", "-"], stdout=subprocess.PIPE)
    # CONFIRMED WOKRING SETTINGS
    # ps = subprocess.Popen(['sox', '-v', '.9', '-t', 'mp3', './playlist.m3u', '-t', 'wav', '--input-buffer', '80000', '-r', '22050', '-c', '2', '-'], stdout=subprocess.PIPE)

    # Experimental
    #ps = subprocess.Popen(['sox', '-v', '.9', '-t', 'mp3', './playlist.m3u', '-t', 'wav', '--input-buffer', '80000', '-r', '44100', '-c', '2', '-'], stdout=subprocess.PIPE)
    with open("playlist.m3u", "r") as file:
        for filename in file:
            ps = subprocess.Popen(['sox', '-t', 'mp3', filename.rstrip(), '-t', 'wav', '--input-buffer', '80000', '-'], stdout=subprocess.PIPE)
            # TODO: display what song is playing on the PS and RT range
            # https://github.com/ChristopheJacquet/PiFmRds
            output = subprocess.Popen(["sudo", "./dependencies/core/pi_fm_rds", "-freq", BROADCAST_FREQUENCY, "-audio", "-"], stdin=ps.stdout)
            print("Closing sox stdout")
            print("Waiting on sox process to finish")
            ps.wait()
            print("Transmission broadcasting")
            output.wait()


# "ffmpeg -i "+arg.song_file+" "+"-f s16le -ar 22.05k -ac 1 - | sudo ./fm_transmitter -f"+" "+frequency+" "+" - "
# sox -v .9 -t mp3 ../Music/tmp/*.mp3 -t wav --input-buffer 80000 -r 22050 -c 1 - | sudo ./fm_transmitter -f 93.8 -
if __name__ == "__main__":
    main()
