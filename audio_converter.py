from os import path
from pydub import AudioSegment

def m4a_to_wav (src, dest):
    sound = AudioSegment.from_file(src)
    sound.export(dest, format="wav")