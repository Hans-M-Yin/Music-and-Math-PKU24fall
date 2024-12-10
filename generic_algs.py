from music21 import *
import random

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

def operator_shifttone (melody1:stream, melody2:stream) -> stream.Stream:
    target_key = key.Key(melody2[0])
    interval = target_key.tonic.transpose(melody1[0].tonic)  # 找到目标调性音高的音程
    s_transposed = stream.Stream(melody1).transpose(interval)
    s_transposed[0] = key.Key(melody2[0])
    return s_transposed

def operator_shifttone(melody:stream) -> stream.Stream:
    random_key = key.Key(random_key_name = random.choice(keys))
    interval = random_key.tonic.transpose(melody[0].tonic)  # 找到目标调性音高的音程
    s_transposed = stream.Stream(melody).transpose(interval)
    s_transposed[0] = key.Key(random_key)

def operator_crossover(melody1:stream, melody2:stream):

    melody1 = operator_shifttone(melody1, melody2)

    random_length = random.randint(2, 32)
    random_start1 = random.randint(0,32-random_length)
    random_end1 = random_start1 + random_length
    random_start2 = random.randint(0,32-random_length)
    random_end2 = random_start2 + random_length

    cur1 = 0
    cur2 = 0

    s_1 = stream.Stream()
    m_1 = stream.Stream()
    e_1 = stream.Stream()
    s_2 = stream.Stream()
    m_2 = stream.Stream()
    e_2 = stream.Stream()

    for n in melody1.notes:
        if cur1 + n.quarterLength <= random_start1:
            s_1.append(n)
        elif cur1 < random_start1 and cur1 + n.quarterLength > random_start1:
            s_1.append(note.Note(n.pitch, random_start1-cur1))
            if cur1 + n.quarterLength <= random_end1:
                m_1.append(note.Note(n.pitch, cur1 + n.quarterLength - random_start1))
            else:
                m_1.append(note.Note(n.pitch, random_end1 - random_start1))
                e_1.append(note.Note(n.pitch, cur1 + n.quarterLength - random_end1))
        elif cur1 >= random_start1 and cur1 + n.quarterLength <= random_end1:
            m_1.append(n)
        elif cur1 < random_end1 and cur1 + n.quarterLength > random_end1:
            m_1.append(note.Note(n.pitch, random_end1-cur1))
            e_1.append(note.Note(n.pitch, cur1 + n.quarterLength - random_end1))
        elif cur1 > random_end1:
            e_1.append(n)
        cur1+=n.quarterLength

    for n in melody2.notes:
        if cur2 + n.quarterLength <= random_start2:
            s_2.append(n)
        elif cur2 < random_start2 and cur2 + n.quarterLength > random_start2:
            s_2.append(note.Note(n.pitch, random_start2-cur2))
            if cur2 + n.quarterLength <= random_end2:
                m_2.append(note.Note(n.pitch, cur2 + n.quarterLength - random_start2))
            else:
                m_2.append(note.Note(n.pitch, random_end2 - random_start2))
                e_2.append(note.Note(n.pitch, cur2 + n.quarterLength - random_end2))
        elif cur2 >= random_start2 and cur2 + n.quarterLength <= random_end2:
            m_2.append(n)
        elif cur2 < random_end2 and cur2 + n.quarterLength > random_end2:
            m_2.append(note.Note(n.pitch, random_end2-cur2))
            e_2.append(note.Note(n.pitch, cur2 + n.quarterLength - random_end2))
        elif cur2 > random_end2:
            e_2.append(n)
        cur2+=n.quarterLength
    
    n_1 = s_1 + m_2 + e_1
    n_2 = s_2 + m_1 + e_2
    n_1.insert(0,key.Key(melody2[0]))
    n_2.insert(0,key.Key(melody2[0]))
    return (n_1, n_2)

def operator_reflection(melody:stream) -> stream.Stream:

    ns = stream.Stream()
    pivot_pitch = key.Key(random_key_name = random.choice(keys)).tonic
    for n in melody.notes:
        reflected_pitch = pivot_pitch.transpose(-1 * (n.pitch.midi - pivot_pitch.midi))
        reflected_note = note.Note(reflected_pitch, quarterLength=n.quarterLength)
        ns.append(reflected_note)
    
    nk = ns.analyze('key')
    ns.insert(0,nk)
    return ns

def operator_inversion(melody:stream) -> stream.Stream:

    total = len(melody.notes)
    rand_start = random.randint(0,total)
    rand_end = random.randint(rand_start+1, total+1)

    cnt=0
    ns = stream.Stream()
    ns.append(melody[0])
    for n in melody.notes:
        if cnt<rand_start or cnt > rand_end:
            ns.append(n)
        if cnt >= rand_start and cnt < rand_end:
            ns.insert(rand_start,n)
        cnt += 1
    return ns

def call_operator (melody1:stream, melody2:stream) -> stream.Stream:
    op = random.randint(0,3)
    if op == 0:
        return operator_crossover(melody1, melody2)
    elif op == 1:
        return operator_reflection(melody1)
    else
        return operator_inversion(melody1)

def run_generic_algorithm(melodies:list[stream.Stream], iterations = 100, criteria = 1.0, total = 15, fraction = 0.7) -> stream:
    iter = 0
    best_performance = 100.0

    population = []
    for strm in melodies:
        population.append(stream_with_score(strm))
    while iter < iterations and best_performance > criteria:
        population = sorted(population, key=lambda x: x.score)
        population = population[:total]
        best_performance = population[0].score

        for i in range(int(total*fraction)-1):
            n_strm = call_operator(population[i], population[i+1])
            population.append(stream_with_score(n_strm))

    return population[0].stream