from music21 import *
from music_to_vector import *
from vector_to_melody import *

if __name__ == "__main__":
    melodies = musicTxt_to_vector()
    settings = environment.UserSettings()
    s = vector_to_stream(melodies[13][0], melodies[13][1])
    s.show('musicxml', app = r'C:\\Program Files\\MuseScore 4\\bin\\MuseScore4.exe')