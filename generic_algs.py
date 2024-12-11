from music21 import *
import random
import numpy as np

keys = [
    'C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B',  # 大调
    'Cm', 'C#m', 'Dm', 'D#m', 'Em', 'Fm', 'F#m', 'Gm', 'G#m', 'Am', 'A#m', 'Bm'  # 小调
]

class stream_with_score:
    def __init__(self, strm):
        self.stream = strm
        self.score = fitness_function(strm)
    

def fitness_function (melody:stream) -> float:
    return 0.0

def operator_shifttone_2 (melody1:stream, melody2:stream) -> stream.Stream:
    # print(melody1[0])
    target_key = key.Key(melody2[0].tonic, melody2[0].mode)
    inter = interval.Interval(melody1[0].tonic, target_key.tonic)
    s_transposed = melody1.transpose(inter)
    return octave_normalize(s_transposed)

def operator_shifttone_1(melody:stream) -> stream.Stream:
    random_key = key.Key(random_key_name = random.choice(keys))
    interval = random_key.tonic.transpose(melody[0].tonic)  # 找到目标调性音高的音程
    s_transposed = stream.Stream(melody).transpose(interval)
    s_transposed[0] = key.Key(random_key)

def handle_crossover(melody1:stream, random_start1: int, random_end1: int):
    cur1 = 0
    s_1 = stream.Stream()
    m_1 = stream.Stream()
    e_1 = stream.Stream()
    for i in range(1,len(melody1)):
        n = melody1[i]
        if isinstance(n,note.Note):
            if cur1 + n.quarterLength*2 <= random_start1:
                s_1.append(n)
            elif cur1 < random_start1 and cur1 + n.quarterLength*2 > random_start1:
                s_1.append(note.Note(n.pitch, quarterLength = (random_start1-cur1)/2))
                if cur1 + n.quarterLength*2 <= random_end1:
                    m_1.append(note.Note(n.pitch, quarterLength = (cur1 + n.quarterLength*2 - random_start1)/2))
                else:
                    m_1.append(note.Note(n.pitch, quarterLength = (random_end1 - random_start1)/2))
                    e_1.append(note.Note(n.pitch, quarterLength = (cur1 + n.quarterLength*2 - random_end1)/2))
            elif cur1 >= random_start1 and cur1 + n.quarterLength*2 <= random_end1:
                m_1.append(n)
            elif cur1 < random_end1 and cur1 + n.quarterLength*2 > random_end1:
                m_1.append(note.Note(n.pitch, quarterLength = (random_end1-cur1)/2))
                e_1.append(note.Note(n.pitch, quarterLength = (cur1 + n.quarterLength*2 - random_end1)/2))
            elif cur1 >= random_end1:
                e_1.append(n)
        elif isinstance(n,note.Rest):
            if cur1 + n.quarterLength*2 <= random_start1:
                s_1.append(n)
            elif cur1 < random_start1 and cur1 + n.quarterLength*2 > random_start1:
                s_1.append(note.Rest(quarterLength = (random_start1-cur1)/2))
                if cur1 + n.quarterLength*2 <= random_end1:
                    m_1.append(note.Rest(quarterLength = (cur1 + n.quarterLength*2 - random_start1)/2))
                else:
                    m_1.append(note.Rest(quarterLength = (random_end1 - random_start1)/2))
                    e_1.append(note.Rest(quarterLength = (cur1 + n.quarterLength*2 - random_end1)/2))
            elif cur1 >= random_start1 and cur1 + n.quarterLength*2 <= random_end1:
                m_1.append(n)
            elif cur1 < random_end1 and cur1 + n.quarterLength*2 > random_end1:
                m_1.append(note.Rest(quarterLength = (random_end1-cur1)/2))
                e_1.append(note.Rest(quarterLength = (cur1 + n.quarterLength*2 - random_end1)/2))
            elif cur1 >= random_end1:
                e_1.append(n)
        cur1+=n.quarterLength*2
    
    return (s_1, m_1, e_1)



def operator_crossover(melody1:stream, melody2:stream):
    
    # melody1.show('musicxml', app = r'C:\\Program Files\\MuseScore 4\\bin\\MuseScore4.exe')
    # melody2.show('musicxml', app = r'C:\\Program Files\\MuseScore 4\\bin\\MuseScore4.exe')
    melody1 = operator_shifttone_2(melody1, melody2)
    
    random_length = random.randint(2, 30)
    random_start1 = random.randint(0,32-random_length)
    random_end1 = random_start1 + random_length
    random_start2 = random.randint(0,32-random_length)
    random_end2 = random_start2 + random_length
    
    s_1, m_1, e_1 = handle_crossover(melody1, random_start1, random_end1)
    s_2, m_2, e_2 = handle_crossover(melody2, random_start2, random_end2)
    
    
    n_1 = stream.Stream()
    n_2 = stream.Stream()

    for elem in s_1:
        n_1.append(elem)

    for elem in m_2:
        n_1.append(elem)

    for elem in e_1:
        n_1.append(elem)
    
    for elem in s_2:
        n_2.append(elem)

    for elem in m_1:
        n_2.append(elem)

    for elem in e_2:
        n_2.append(elem)
    
    # print(n_1.quarterLength)
    # print(n_2.quarterLength)
    n_1.insert(0,key.Key(melody2[0].tonic, melody2[0].mode))
    n_2.insert(0,key.Key(melody2[0].tonic, melody2[0].mode))
    # n_1.show('musicxml', app = r'C:\\Program Files\\MuseScore 4\\bin\\MuseScore4.exe')
    # n_2.show('musicxml', app = r'C:\\Program Files\\MuseScore 4\\bin\\MuseScore4.exe')
    return (octave_normalize(n_1), octave_normalize(n_2))

def operator_reflection(melody:stream) -> stream.Stream:

    ns = stream.Stream()
    pivot_pitch = key.Key(random_key_name = random.choice(keys)).tonic
    # print(pivot_pitch)
    for i in range(1,len(melody)):
        if isinstance(melody[i], note.Note):
            reflected_pitch = pivot_pitch.transpose(-1 * (melody[i].pitch.midi - pivot_pitch.midi))
            # print(reflected_pitch)
            reflected_note = note.Note(reflected_pitch, quarterLength=melody[i].quarterLength)
            # print(reflected_note)
            ns.append(reflected_note)
        else:
            ns.append(melody[i])
    
    nk = ns.analyze('key')
    ns.insert(0,nk)
    return octave_normalize(ns)

def operator_inversion(melody:stream) -> stream.Stream:

    total = len(melody)
    rand_start = random.randint(0,total-2)
    rand_end = random.randint(rand_start+1, total)

    # print(melody.quarterLength)
    ns = stream.Stream()
    ns.append(key.Key(melody[0].tonic, melody[0].mode))
    flag = False
    m = stream.Stream()
    for w in range(1,total):
        if w<rand_start:
            ns.append(melody[w])
        elif w >= rand_start and w < rand_end:
            m.append(melody[w])
        else:
            if flag == False:
                l = len(m)
                for i in range(l):
                    ns.append(m[l-i-1])
                flag = True
            ns.append(melody[w])
    if flag == False:
        l = len(m)
        for i in range(l):
            ns.append(m[l-i-1])
    return octave_normalize(ns)

def octave_normalize(melody:stream) -> stream.Stream:
    lowest_note = None
    highest_note = None
    
    for element in melody.notes:  # 使用 flatten() 确保访问所有音符
        # print("haha")
        if isinstance(element, note.Note):  # 确保是音符对象
            if lowest_note is None or element.pitch < lowest_note.pitch:
                lowest_note = element
            elif highest_note is None or element.pitch < highest_note.pitch:
                highest_note = element

    transform = 0
    
    if lowest_note.pitch > pitch.Pitch('C5'):
        transform = 4 - lowest_note.pitch.octave
    elif highest_note.pitch < pitch.Pitch('C4'):
        transform = 4 - highest_note.pitch.octave
    melody = melody.transpose(transform * 12)
    return melody

def operator_basic_mutation(melody:stream) -> stream.Stream:
    
    size = random.randint(1,len(melody)-2)
    
    change_mask = np.random.choice(range(1, len(melody)-1), size=size, replace=False)
    change_mask.sort()

    change_delta = np.round(np.random.normal(0, 2, len(change_mask))).astype(int)
    # print(len(change_mask))
    # print(len(change_delta))
    temp = []
    for i in range(len(change_mask)):
        if isinstance(melody[int(change_mask[i])], note.Note):
            temp.append(melody[int(change_mask[i])].transpose(int(change_delta[i])))
        else:
            temp.append(melody[int(change_mask[i])])
    ns = stream.Stream()
    ns.append(key.Key(melody[0].tonic, melody[0].mode))
    cur = 0
    for i in range(1,len(melody)):
        if cur < len(temp) and i == change_mask[cur]:
            ns.append(temp[cur])
            cur += 1
        else:
            ns.append(melody[i])
    return octave_normalize(ns)

def run_generic_algorithm(melodies:list[stream.Stream], iterations = 1, criteria = 1.0, total = 15, fraction = 0.7) -> stream:
    iter = 0
    best_performance = 100.0

    population = []
    for strm in melodies:
        population.append(stream_with_score(strm))
    while iter < iterations and best_performance > criteria:
        population = sorted(population, key=lambda x: x.score)
        population = population[:total]
        best_performance = population[0].score

        for i in range(0,100):
            op = random.randint(0,4)
            
            if op == 0:
                print(0)
                rd2 = random.randint(0,len(population)-1)
                ns1, ns2 = operator_crossover(population[i].stream, population[rd2].stream)
                population.append(stream_with_score(ns1))
                population.append(stream_with_score(ns2))
                print(ns1.quarterLength)
                print(ns2.quarterLength)
                # ns1.show('musicxml', app = r'C:\\Program Files\\MuseScore 4\\bin\\MuseScore4.exe')
                # ns2.show('musicxml', app = r'C:\\Program Files\\MuseScore 4\\bin\\MuseScore4.exe')
            elif op == 1:
                print(1)
                ns = operator_reflection(population[i].stream)
                # print(ns.quarterLength)
                population.append(stream_with_score(ns))
                # ns.show('musicxml', app = r'C:\\Program Files\\MuseScore 4\\bin\\MuseScore4.exe')
            elif op == 2:
                print(2)
                ns = operator_inversion(population[i].stream)
                # print(ns.quarterLength)
                population.append(stream_with_score(ns))
                ns.show('musicxml', app = r'C:\\Program Files\\MuseScore 4\\bin\\MuseScore4.exe')
            else:
                print(3)
                ns = operator_basic_mutation(population[i].stream)
                print(ns.quarterLength)
                population.append(stream_with_score(ns))
                # ns.show('musicxml', app = r'C:\\Program Files\\MuseScore 4\\bin\\MuseScore4.exe')

    return population[0].stream