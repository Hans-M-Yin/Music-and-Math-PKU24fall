from music21 import *
from music_to_vector import *
from vector_to_melody import *
from generic_algs import *

if __name__ == "__main__":
    # configure.run()
    vecs = musicTxt_to_vector()
    melodies = []
    for i in range(0,len(vecs)):
        melodies.append(vector_to_stream(vecs[i][0], vecs[i][1]))
    s = run_generic_algorithm(melodies)
    print('#######',s)
    for ss in s:
        ss.show('musicxml')
    #score = fitness_function(ss)
    #print(f'########{score}########')
    # s.show('musicxml', app = r'C:\\Program Files\\MuseScore 4\\bin\\MuseScore4.exe')
