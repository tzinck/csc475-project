import sys
import numpy as np
import aubio
import matplotlib.pyplot as plt

def beat_detect(filename, win_s=512, hop_s=256):
    samplerate = 0

    s = aubio.source(filename, samplerate, hop_s)
    samplerate = s.samplerate
    o = aubio.tempo("default", win_s, hop_s, samplerate)

    # tempo detection delay, in samples
    # default to 4 blocks delay to catch up with
    delay = 4. * hop_s

    # list of beats, in samples
    beats = []

    # total number of frames read
    total_frames = 0
    while True:
        samples, read = s()
        is_beat = o(samples)
        if is_beat:
            this_beat = int(total_frames - delay + is_beat[0] * hop_s)
            beats.append(this_beat)
        total_frames += read
        if read < hop_s: break
    return beats

def onset_detect(filename, win_s=512, hop_s=256):
    samplerate = 0

    s = aubio.source(filename, samplerate, hop_s)
    samplerate = s.samplerate

    o = aubio.onset("default", win_s, hop_s, samplerate)

    # list of onsets, in samples
    onsets = []

    # total number of frames read
    total_frames = 0
    while True:
        samples, read = s()
        if o(samples):
            onsets.append(o.get_last())
        total_frames += read
        if read < hop_s: break
    return onsets

def is_close(num1, num2, percent_range):
    upper = 1 + percent_range/100
    lower = 1 - percent_range/100
    if num1 >= (num2 * upper) or num1 <= (num2 * lower):
        return False
    return True

def quantize_beats(beats):
    gap = beats[1] - beats[0]
    print ("GAP = {}".format(gap / 22050))
    rhythm1 = [beats[0]]

    p = beats[0]
    for i in range(1, len(beats)-1):
        next_beat = p + gap

        j = i
        while (j < len(beats) and next_beat >= beats[j]):
            print ("checking {0} vs {1}".format(next_beat/22050, beats[j]/22050))
            if (is_close(next_beat, beats[j], 10) and beats[j] not in rhythm1):
                rhythm1.append(beats[j])
            j = j+1

        # OPTION 1
        #p = next_beat
        # OPTION 2
        p = beats[i]
        
        print ("p = {}".format(p/22050))

        #print (next_beat / 22050)

    print ("rhythm1 = {0}".format(np.array(rhythm1) / 22050))

def main():
    print("Polyrhythmic Beat Detection")

    filename = "input/120BPM34.wav"

    if(len(sys.argv) > 1):
        filename = sys.argv[1]
    
    print("Onsets:\n")
    onsets = onset_detect(filename)
    onsets_t = np.array(onsets) / 44100
    # temp
    onsets = np.delete(onsets, 1)
    onsets_t = np.delete(onsets_t, 1)
    print(np.array(onsets) / 22050)

    # plot onsets
    #for xc in onsets_t:
    #    plt.axvline(x=xc)
    #plt.show()

    #beats = beat_detect(filename)
    #print("\nBeats:\n")
    #print(np.array(beats) / 22050)

    quantize_beats(onsets)

    

if __name__ == "__main__":
    main()

