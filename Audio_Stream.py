
from flask import Flask, Response, render_template
import pyaudio
import wave

app = Flask(__name__, template_folder="template")

FORMAT = pyaudio.paInt16
CHANNELS = 2
RATE = 44100
CHUNK = 1024

audio_stream = pyaudio.PyAudio()

# Load the recorded audio file
audio_file_path = "path/to/your/recorded_audio.wav"
wf = wave.open(audio_file_path, 'rb')

def genHeader(sampleRate, bitsPerSample, channels):
    datasize = wf.getnframes() * wf.getsampwidth()
    o = bytes("RIFF",'ascii')                                               # (4byte) Marks file as RIFF
    o += (datasize + 36).to_bytes(4,'little')                               # (4byte) File size in bytes excluding this and RIFF marker
    o += bytes("WAVE",'ascii')                                              # (4byte) File type
    o += bytes("fmt ",'ascii')                                              # (4byte) Format Chunk Marker
    o += (16).to_bytes(4,'little')                                          # (4byte) Length of above format data
    o += (1).to_bytes(2,'little')                                           # (2byte) Format type (1 - PCM)
    o += (channels).to_bytes(2,'little')                                    # (2byte)
    o += (sampleRate).to_bytes(4,'little')                                  # (4byte)
    o += (sampleRate * channels * bitsPerSample // 8).to_bytes(4,'little')  # (4byte)
    o += (channels * bitsPerSample // 8).to_bytes(2,'little')               # (2byte)
    o += (bitsPerSample).to_bytes(2,'little')                               # (2byte)
    o += bytes("data",'ascii')                                              # (4byte) Data Chunk Marker
    o += (datasize).to_bytes(4,'little')                                    # (4byte) Data size in bytes
    return o

def Sound():
    bitspersample = 16
    wav_header = genHeader(RATE, bitspersample, 2)
    first_run = True
    while True:
        if first_run:
            data = wav_header + wf.readframes(CHUNK)
            first_run = False
        else:
            data = wf.readframes(CHUNK)
        yield data

@app.route('/')
def index():
    return render_template("Audio.html")

@app.route("/audio")
def audio():
    return Response(Sound())

app.run(host="127.0.0.1", port=5454, threaded=True)
