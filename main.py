import audio
import shutil
from os import listdir, sep, remove
from os.path import isfile, join, splitext
from audio_converter import m4a_to_wav

PATH = 'processar'
WORK = 'work'
TEXT = 'textos'
DONE = 'processado'

# Read audio files @ /audio
files = [f for f in listdir(path=PATH) if isfile(join(PATH, f))]

waves_to_process = []
# Convert to wav
for m4a in files:
    filename = splitext(m4a)[0]
    source_file = f'{PATH}{sep}{m4a}'
    destination_file = f'{WORK}{sep}{filename}.wav'
    move_to = f'{DONE}{sep}{m4a}'

    m4a_to_wav(source_file, destination_file)
    waves_to_process.append({"file": destination_file, "filename": filename})
    shutil.move(source_file, move_to)

for wav in waves_to_process:
    wav_source_file = wav.get("file")
    wav_filename = wav.get("filename")
    audio.speech_to_text(wav_source_file, f'{TEXT}{sep}{wav_filename}.txt')
    remove(wav_source_file)