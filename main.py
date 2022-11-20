import pyaudio
import sys
import numpy as np
import aubio
import pydirectinput as pdi
import subprocess

# initialise pyaudio
p = pyaudio.PyAudio()

# open stream
buffer_size = 1024
pyaudio_format = pyaudio.paFloat32
n_channels = 1
samplerate = 44100

stream = p.open(format=pyaudio_format,
                channels=n_channels,
                rate=samplerate,
                input=True,
                frames_per_buffer=buffer_size)

if len(sys.argv) > 1:
    # record 5 seconds
    output_filename = sys.argv[1]
    record_duration = 5 # exit 1
    outputsink = aubio.sink(sys.argv[1], samplerate)
    total_frames = 0
else:
    # run forever
    outputsink = None
    record_duration = None

# setup pitch
tolerance = 0.8
win_s = 4096 # fft size
hop_s = buffer_size # hop size
pitch_o = aubio.pitch("default", win_s, hop_s, samplerate)
pitch_o.set_unit("midi")
pitch_o.set_tolerance(tolerance)

walk = False
jump = False
squat = False
right = False
left = False
mouseup = False
mousedown = False
zero = False

print("*** starting recording")

while True:
    try:
        audiobuffer = stream.read(buffer_size)
        signal = np.fromstring(audiobuffer, dtype=np.float32)

        pitch = pitch_o(signal)[0]

        if 72 < pitch < 73 and walk == False:
            print('w')
            pdi.keyDown('w')
            walk = True
            jump = False
            squat = False
            left = False
            right = False
            zero = False

        elif 74 < pitch < 74.5 and jump == False:
            print('space')
            pdi.press('space')
            walk = False
            jump = True
            squat = False
            left = False
            right = False
            zero = False

        elif 75.5 < pitch < 76.5 and squat == False:
            print('shift')
            pdi.keyDown('shift')
            walk = False
            jump = False
            squat = True
            left = False
            right = False
            zero = False
        
        elif 77 < pitch < 78 and left == False:
            print('left')
            walk = False
            jump = False
            squat = False
            left = True
            right = False
            zero = False
            moveleft = subprocess.Popen(["python", "mouseleft.py"], stdin=None, stdout=None, stderr=None, close_fds=True)
            
        elif 78.5 < pitch < 79.5 and right == False:
            print('right')
            walk = False
            jump = False
            squat = False
            left = False
            right = True
            zero = False
            moveright = subprocess.Popen(["python", "mouseright.py"], stdin=None, stdout=None, stderr=None, close_fds=True)
        
        elif int(pitch) == 0 and zero == False:
            
            try:
                pollleft = moveleft.poll()
                if pollleft is None:
                    moveleft.terminate()
            except:
                pass

            try:
                pollright = moveright.poll()
                if pollright is None:
                    moveright.terminate()
            except:
                pass
                
            pdi.keyUp('w')
            pdi.keyUp('shift')
            walk = False
            jump = False
            squat = False
            left = False
            right = False
            zero = True 

        #print("{}".format(pitch))

        if outputsink:
            outputsink(signal, len(signal))

        if record_duration:
            total_frames += len(signal)
            if record_duration * samplerate < total_frames:
                break
    except KeyboardInterrupt:
        print("*** Ctrl+C pressed, exiting")
        break

print("*** done recording")
stream.stop_stream()
stream.close()
p.terminate()