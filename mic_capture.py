__author__ = 'thauser'

import pyaudio
import pocketsphinx as ps
from espeak import espeak
import time


#Buffer size in bytes
CHUNK=1024

# the audio format. some kind of magic
FORMAT= pyaudio.paInt16

# audio channels to record on
CHANNELS=1

# sample rate in hz
RATE=16000

# number of seconds to record
RECORD_SECS=5


# hmmd = '/usr/share/pocketsphinx/model/hmm/en_US/hub4wsj_sc_8k/'
# lmd = '/usr/share/pocketsphinx/lm/en_US/hub4.5000.DMP'
# dictd = '/usr/share/pocketsphinx/model/lm/en_US/hub4.5000.dic'

d = ps.Decoder()

p = pyaudio.PyAudio()

stream = p.open(format=FORMAT, frames_per_buffer=CHUNK, input=True, rate=RATE, channels=CHANNELS)
frames = []
for i in range(0, int(RATE / CHUNK * RECORD_SECS)):
    data = stream.read(CHUNK)
    frames.append(data)

print(frames)

d.start_utt()

string=''

for frame in frames:
    string+=frame

d.process_raw(string, False, False)
text = d.get_hyp()[0]
print (text)
if text:
    espeak.synth(text)
#stream.start_stream()

time.sleep(10)

# while True:
#     buf = stream.read(CHUNK)
#     d.process_raw(buf, False, False)
#     text = d.get_hyp()[0]
#     if text:
#         espeak.synth(text)

d.end_utt()
stream.stop_stream()
stream.close()
p.terminate()
