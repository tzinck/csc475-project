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

def is_close(num1, num2, max_diff, percent=20):
    diff = abs(num1 - num2)
    return diff <= max_diff*percent/100
    '''
    upper = 1 + percent_range/100
    lower = 1 - percent_range/100
    if num1 >= (num2 * upper) or num1 <= (num2 * lower):
        return False
    return True
    '''

def quantize_beats(beats):
    gap = beats[1] - beats[0]
    print ("GAP = {}".format(gap / 22050))
    rhythm1 = [beats[0]]

    p = beats[0]
    for i in range(1, len(beats)-1):
        
        next_beat = p + gap

        j = i
        while (j < len(beats)):
            #print ("checking {0} vs {1}".format(next_beat/22050, beats[j]/22050))
            if (is_close(next_beat, beats[j], gap) and beats[j] not in rhythm1):
                #print ("{} IS GOOD.".format(beats[j] / 22050))
                rhythm1.append(beats[j])
                p = beats[j]
                break
            else:
                p = rhythm1[-1]

            if beats[j] > next_beat:
                print ("lol")
                break

            j = j + 1

        # OPTION 1
        #p = next_beat
        # OPTION 2
        #p = beats[i]
        
        #print ("p = {}".format(p/22050))

        #print (next_beat / 22050)

    print ("rhythm1 = {0}".format(np.array(rhythm1) / 22050))

    '''
    # plot rhythms
    plt.figure(figsize=(18, 2))
    plt.xlim(0, 20)
    for xc in rhythm1:
        plt.axvline(x=xc/22050, color='red')
    plt.draw()
    '''

    rhythm2 = temp_q2(beats, rhythm1)

    return (rhythm1, rhythm2)


def temp_q2(beats, rhythm1):
    for b in beats:
        if b not in rhythm1:
            first = b
            break
        
    gap = first - beats[0]
    print ("GAP = {}".format(gap / 22050))
    rhythm2 = [beats[0]]

    p = beats[0]
    for i in range(1, len(beats)-1):
        
        next_beat = p + gap

        j = i
        while (j < len(beats)):
            #print ("checking {0} vs {1}".format(next_beat/22050, beats[j]/22050))
            if (is_close(next_beat, beats[j], gap) and beats[j] not in rhythm2):
                #print ("{} IS GOOD.".format(beats[j] / 22050))
                rhythm2.append(beats[j])
                p = beats[j]
                break
            else:
                p = rhythm2[-1]
            j = j+1

    print ("rhythm2 = {0}".format(np.array(rhythm2) / 22050))

    '''
    # plot rhythms
    plt.figure(figsize=(18, 2))
    plt.xlim(0, 20)
    for xc in rhythm2:
        plt.axvline(x=xc/22050, color='green')
    plt.draw()
    '''

    return rhythm2

def main():
    print("Polyrhythmic Beat Detection")

    filename = "input/120BPM34long.wav"

    if(len(sys.argv) > 1):
        filename = sys.argv[1]
    
    print("Onsets:\n")
    onsets = onset_detect(filename)
    onsets_t = np.array(onsets) / 22050
    # temp
    #onsets = np.delete(onsets, 1)
    #onsets_t = np.delete(onsets_t, 1)
    print(np.array(onsets) / 22050)

    '''
    # plot onsets
    plt.figure(figsize=(18, 2))
    plt.xlim(0, 20)
    for xc in onsets_t:
        plt.axvline(x=xc)
    plt.draw()
    '''
    
    #beats = beat_detect(filename)
    #print("\nBeats:\n")
    #print(np.array(beats) / 22050)

    (rhythm1, rhythm2) = quantize_beats(onsets)

    # Two subplots, the axes array is 1-d
    f, (poly, r1, r2) = plt.subplots(3, sharex=True)
    for xc in onsets_t:
        poly.axvline(x=xc)

    for xc in rhythm1:
        r1.axvline(x=xc/22050, color='red')

    for xc in rhythm2:
        r2.axvline(x=xc/22050, color='green')

    poly.set_title("Onsets for polyrhythmic 3:4 beat.")
    poly.axes.get_yaxis().set_visible(False)
    r1.axes.get_yaxis().set_visible(False)
    r2.axes.get_yaxis().set_visible(False)
    plt.show()
    

if __name__ == "__main__":
    main()

