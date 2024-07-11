import pyaudio
import time
import numpy as np
from iat_ws_python3 import *
from test import *

RATE = 16000 # 修改采样率为16k
CHUNK = 2048
FORMAT = pyaudio.paInt16 # 16位，+-32768
CHANNELS = 1
RECORD_SECONDS = 3
THRESHOLD = 500
audio = pyaudio.PyAudio()

# 获取设备名称
DEVICE_INDEX= 6
 # 请替换为实际的输入设备名称

stream = audio.open(format=FORMAT,
                    channels=CHANNELS,
                    rate=RATE,
                    input=True,
                    input_device_index=DEVICE_INDEX,
                    frames_per_buffer=CHUNK)

frames = []
silent_frames = 0
flag = 0

def save_pcm(frames):
    filename = "audio.pcm"
    with open(filename, 'wb') as f:
        f.write(b''.join(frames))
        print(f"Saved file: {filename}")

def detect_silence(data):
    audio_data = np.frombuffer(data, dtype=np.int16)
    max_val = np.max(np.abs(audio_data))
    return max_val < THRESHOLD

print("Listening...")

try:
    while True:
        data = stream.read(CHUNK)
        frames.append(data)

        if detect_silence(data):
            silent_frames += 1
        else:
            flag = 1
            silent_frames = 0

        if silent_frames >= int(RATE / CHUNK * RECORD_SECONDS):
            stream.stop_stream()
            print("Silence detected.")
            if flag == 1:
                save_pcm(frames)
                text = run()
                if text == "None":
                    continue
                fl = act(text)
                if fl == False:
                    print("No action!")

            # ...
                flag = 0
            print("Listening...")
            stream.start_stream()  # clear
            frames = []
            silent_frames = 0

except KeyboardInterrupt:
    if frames and flag == 1:
        save_pcm(frames)
        print("Recording stopped.")

stream.stop_stream()
stream.close()
audio.terminate()
