import numpy as np
import aubio

def beat_detect(filename, win_s=512, hop_s = 256):
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

def main():
    print("Polyrhythmic Beat Detection")
    test_beats = beat_detect("input/classical.00000.wav")
    print(len(test_beats))

if __name__ == "__main__":
    main()

