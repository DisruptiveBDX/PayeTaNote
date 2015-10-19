import sys
import math
import struct
import pyaudio


def play_tone(frequency, amplitude, duration, fs, stream):
  N = int(fs / frequency)
  T = int(frequency * duration)  # repeat for T cycles
  dt = 1.0 / fs
  # 1 cycle
  tone = (amplitude * math.sin(2 * math.pi * frequency * n * dt) for n in xrange(N))
    # todo: get the format from the stream; this assumes Float32
  data = ''.join(struct.pack('f', samp) for samp in tone)
  for n in xrange(T):
    stream.write(data)

fs = int(sys.argv[1])
print fs
p = pyaudio.PyAudio()
stream = p.open(
  format=pyaudio.paFloat32,
  channels=1,
  rate=fs,
  output=True)

# play the C major scale
play_tone(float(sys.argv[2]), 0.5, float(sys.argv[3]), fs, stream)

stream.close()
p.terminate()