import subprocess
import os
import random

# Globals
RUNTIME_DIR = "/home/pi/PirateShip/"
AUDIO_FILES_DIRECTORY = RUNTIME_DIR + "music/"
PI_FM_RDS = RUNTIME_DIR + "dependencies/core/pi_fm_rds_working"
BROADCAST_FREQUENCY = "99.5" #"105.5"

def main():
    # Do stuff
    build_playlist()
    play_playlist()


def build_playlist():
    files = os.listdir(AUDIO_FILES_DIRECTORY)
    random.shuffle(files)

    with open(RUNTIME_DIR + "playlist.m3u", "w") as file:
        for filename in files:
            # Skip comment file
            if filename.startswith('#'):
                continue
            else:
                file.write(AUDIO_FILES_DIRECTORY + filename + "\n")


def play_playlist():
    print("Playing playlist on frequency " + BROADCAST_FREQUENCY)

    # Alternative audio processing, not sure if it will function with PI_FM_RDS but it might with some tweaking
    #ps = subprocess.Popen(["ffmpeg", "-nostdin", "-i", file, "-f", "s16le", "-ar", "22.05k", "-ac", "1", "-"], stdout=subprocess.PIPE)

    with open(RUNTIME_DIR + "playlist.m3u", "r") as file:
        # Create the PI FM RDS subprocess asynchronously so we can bind the sox stdout to this subprocess input pipe below.
        output = subprocess.Popen(["sudo", PI_FM_RDS, "-freq", BROADCAST_FREQUENCY, "-audio", "-"], stdin=subprocess.PIPE, stdout=subprocess.DEVNULL)

        for filename in file:

            if output.poll() is not None:
                # In case for whatever reason the subprocess gets killed after the initial processing, spawn a new one.
                output = subprocess.Popen(["sudo", PI_FM_RDS, "-freq", BROADCAST_FREQUENCY, "-audio", "-"],stdin=subprocess.PIPE, stdout=subprocess.DEVNULL)

            # Processes mp3 to stdout (piped into the PI_FM_RDS process) using an input buffer.
            ps = subprocess.Popen(['sox', '-v', '1.3', '-t', 'mp3', (filename.rstrip()), '-t', 'wav', '--input-buffer', '80000', '-r', '44100','-G', '-c', '2', '-'], stdout=output.stdin)

            # TODO: display what song is playing on the PS and RT range
            # https://github.com/ChristopheJacquet/PiFmRds

            print("Processing song: "+filename+"waiting for sox to complete")
            ps.wait()

        print("Playlist complete, waiting for transmission to complete")
        output.wait()

def change_broadcast_frequency():
    raise NotImplementedError


# "ffmpeg -i "+arg.song_file+" "+"-f s16le -ar 22.05k -ac 1 - | sudo ./fm_transmitter -f"+" "+frequency+" "+" - "
# sox -v .9 -t mp3 ../Music/tmp/*.mp3 -t wav --input-buffer 80000 -r 22050 -c 1 - | sudo ./fm_transmitter -f 93.8 -
if __name__ == "__main__":
    main()
