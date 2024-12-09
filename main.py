from music21 import *
from music_to_vector import *
from vector_to_melody import *

if __name__ == "__main__":
    print("hello")
    melodies = musicTxt_to_vector()
    s = vector_to_stream(melodies[0])
    
    s.show('text')