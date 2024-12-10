from music21 import *
from music_to_vector import *
from vector_to_melody import *
from generic_algs import *

if __name__ == "__main__":
    vecs = musicTxt_to_vector()
    melodies = []
    for i in range(0,15):
        melodies.append(vector_to_stream(vecs[i][0], vecs[i][1]))
    s = run_generic_algorithm(melodies)
    # s.show('musicxml', app = r'C:\\Program Files\\MuseScore 4\\bin\\MuseScore4.exe')