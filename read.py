import pyaudio
import time
import numpy as np
from iat_ws_python3 import *


RATE = 16000  # 修改采样率为16k
CHUNK = 1024
FORMAT = pyaudio.paInt16  # 16位，+-32768
CHANNELS = 1
RECORD_SECONDS = 2  # 当沉默时间长于2s时，就自动保存为.pcm文件
THRESHOLD = 1000  # 声音小于这个阈值视为沉默,设置一个合适的值
audio = pyaudio.PyAudio()

# 设置设备索引
DEVICE_INDEX = 1  # 根据设备列表，选择麦克风设备索引

stream = audio.open(format=FORMAT,
                    channels=CHANNELS,
                    rate=RATE,
                    input=True,
                    input_device_index=DEVICE_INDEX,
                    frames_per_buffer=CHUNK)

frames = []
silent_frames = 0  # 记录连续静音的帧数
flag = 0
def save_pcm(frames):
    filename = "audio.pcm"  # 固定文件名
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
            print("Silence detected.")
            if(flag == 1):
                save_pcm(frames)
                text = run()
                # 封装的接口位置
                while( ..!= ..):
                    LLM(text)  
                    xx = return(fl) # 比如在完成动作之后会返回一个flag
                    
                # ...
                flag = 0
            print("Listening...")
            frames = []
            silent_frames = 0

except KeyboardInterrupt:
    if frames and flag == 1:
        save_pcm(frames)
    print("Recording stopped.")

stream.stop_stream()
stream.close()
audio.terminate()
