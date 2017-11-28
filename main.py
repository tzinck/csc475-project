import sys
import numpy as np
import aubio

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
    if num1 >= (num2 * (1 + (percent_range/100))) or num1 <= (num2 * (1 - (percent_range/100))):
        return False
    return True

def quantize_beats(beats):
    return False

def main():
    print("Polyrhythmic Beat Detection")

    filename = "input/metal.00032.wav"

    if(len(sys.argv) > 1):
        filename = sys.argv[1]
    
    print("Onsets:\n")
    onsets = onset_detect(filename)
    print(np.array(onsets) / 22050)

    beats = beat_detect(filename)
    print("\nBeats:\n")
    print(np.array(beats) / 22050)

if __name__ == "__main__":
    main()

