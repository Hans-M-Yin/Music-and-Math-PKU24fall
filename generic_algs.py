from music21 import *
import random
import numpy as np
from collections import Counter

keys = [
    'C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B',  # 大调
    'Cm', 'C#m', 'Dm', 'D#m', 'Em', 'Fm', 'F#m', 'Gm', 'G#m', 'Am', 'A#m', 'Bm'  # 小调
]

class stream_with_score:
    def __init__(self, strm):
        self.stream = strm
        self.score = fitness_function(strm)
    

def fitness_function(melody: stream.Stream) -> float:

    # 音符频率
    all_notes = [element.pitch.name for element in melody.flatten().notes if isinstance(element, note.Note)]
    if not all_notes:
        return 0.0
    note_counts = Counter(all_notes)
    variance = np.var(list(note_counts.values()))
    note_fitness = 1 / (1 + variance) if variance >= 0 else 0.0

    # 音程
    intervals = []
    prev_note = None
    for element in melody.flatten().notes:
        if isinstance(element, note.Note):
            if prev_note is not None:
                try:
                    intvl = interval.Interval(prev_note.pitch, element.pitch).simpleName
                    intervals.append(intvl)
                except Exception as e:
                    print(f"Error calculating interval: {e}")
            prev_note = element
    num_intervals = len(intervals)
    consonant_count = sum(1 for intvl in intervals if intvl in ['P1', 'm3', 'M3', 'P5', 'm6', 'M6', 'P8'])
    interval_fitness = consonant_count / num_intervals if num_intervals > 0 else 0.0

    # 节奏规律性，计算相邻音符的时长差值的方差
    durations = [element.duration.quarterLength for element in melody.flatten().notes if isinstance(element, note.Note)]
    if len(durations) < 2:
        rhythm_fitness = 0.0
    else:
        durations_diff = [durations[i + 1] - durations[i] for i in range(len(durations) - 1)]
        variance_rhythm = np.var(durations_diff)
        rhythm_fitness = 1 / (1 + variance_rhythm) if variance_rhythm >= 0 else 0.0

    # 音高差
    pitches = [element.pitch.midi for element in melody.flatten().notes if isinstance(element, note.Note)]
    if not pitches:
        range_fitness = 0.0
    else:
        pitch_range = max(pitches) - min(pitches)
        if 12 <= pitch_range <= 20:
            range_fitness = 1
        else:
            range_fitness = 1 / (1 + abs(pitch_range - 16))

    # 旋律重复比例
    note_pairs = [(melody.flatten().notes[i].pitch.name, melody.flatten().notes[i + 1].pitch.name)
                  for i in range(len(melody.flatten().notes) - 1) if isinstance(melody.flatten().notes[i], note.Note) and
                  isinstance(melody.flatten().notes[i + 1], note.Note)]
    pair_counts = Counter(note_pairs)
    total_pairs = len(note_pairs)
    repeated_count = sum(count for _, count in pair_counts.items() if count > 1)
    repetition_fitness = 1 - (repeated_count / total_pairs if total_pairs > 0 else 0)

    # 音符时长分布合理性
    if not durations:
        duration_distribution_fitness = 0.0
    else:
        duration_counts = Counter(durations)
        total_duration_count = len(durations)
        probabilities = [count / total_duration_count for count in duration_counts.values()]
        entropy = -np.sum([p * np.log2(p) for p in probabilities if p > 0])
        if entropy >= 0.5 and entropy <= 1.5: 
            duration_distribution_fitness = 1
        else:
            duration_distribution_fitness = 1 / (1 + abs(entropy - 1))

    # 旋律轮廓的平滑性
    if len(pitches) < 2:
        contour_smoothness_fitness = 0.0
    else:
        pitch_diffs = [abs(pitches[i + 1] - pitches[i]) for i in range(len(pitches) - 1)]
        sum_diffs = sum(pitch_diffs)
        contour_smoothness_fitness = 1 / (1 + sum_diffs)

    weight_note = 0.15  # 音符频率权重
    weight_interval = 0.25  # 音程权重
    weight_rhythm = 0.2  # 节奏规律性权重
    weight_range = 0.15  # 音域范围合理性权重
    weight_repetition = 0.1  # 旋律重复性权重
    weight_duration_distribution = 0.1 # 音符时长分布合理性权重
    weight_contour_smoothness = 0.05  # 旋律轮廓平滑性权重
    return (weight_note * note_fitness +
            weight_interval * interval_fitness +
            weight_rhythm * rhythm_fitness +
            weight_range * range_fitness +
            weight_repetition * repetition_fitness
            + weight_duration_distribution * duration_distribution_fitness
            + weight_contour_smoothness * contour_smoothness_fitness)
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


def keyharmony(melody:stream)->stream.Stream:
    k = melody[0]
    for n in melody.notes:
        nstep = n.pitch.step
        rightAccidental = k.accidentalByStep(nstep)
        n.pitch.accidental = rightAccidental
    return melody


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
    return keyharmony(octave_normalize(ns))

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
    for element in melody.notes:  
        if isinstance(element, note.Note):  # 确保是音符对象
            if element.octave is not None:
                if element.octave < 4:
                    element.octave = 4
                elif element.octave > 5:
                    element.octave = 5

    return melody
    
    transform = 0
    
    if lowest_note.pitch > pitch.Pitch('C5'):
        transform = 4 - int(lowest_note.pitch.octave)
    elif highest_note.pitch < pitch.Pitch('C4'):
        transform = 4 - int(highest_note.pitch.octave)
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
    return keyharmony(octave_normalize(ns))

def run_generic_algorithm(melodies:list[stream.Stream], iterations = 3, criteria = 0.95, total = 50) -> stream:
    iter = 0
    best_performance = 0.0

    population = []
    for strm in melodies:
        population.append(stream_with_score(strm))
    oril = len(population)
    ### add
    population = sorted(population, key=lambda x: x.score, reverse=True)
    flag = True
    while iter < iterations:
        # population = sorted(population, key=lambda x: x.score)
        population = population[:total]
        l = len(population)
        ### change parameter
        for i in range(0,l):
            op = random.randint(0,3)
            print(op)
            if op == 0:
                rd2 = random.randint(0,len(population)-1)
                ns1, ns2 = operator_crossover(population[i].stream, population[rd2].stream)
                population.append(stream_with_score(ns1))
                population.append(stream_with_score(ns2))
                assert(ns1.quarterLength == 16)
                assert(ns2.quarterLength == 16)
                # print(population[len(population)-1].score)
                # ns2.show('musicxml', app = r'C:\\Program Files\\MuseScore 4\\bin\\MuseScore4.exe')
            elif op == 1:
                ns = operator_reflection(population[i].stream)
                population.append(stream_with_score(ns))
                assert(ns.quarterLength == 16)
                # print(population[len(population)-1].score)
                # ns.show('musicxml', app = r'C:\\Program Files\\MuseScore 4\\bin\\MuseScore4.exe')
            elif op == 2:
                ns = operator_inversion(population[i].stream)
                population.append(stream_with_score(ns))
                assert(ns.quarterLength == 16)
                # print(population[len(population)-1].score)
                # ns.show('musicxml', app = r'C:\\Program Files\\MuseScore 4\\bin\\MuseScore4.exe')
            else:
                ns = operator_basic_mutation(population[i].stream)
                population.append(stream_with_score(ns))
                assert(ns.quarterLength == 16)
                # print(population[len(population)-1].score)
                # ns.show('musicxml', app = r'C:\\Program Files\\MuseScore 4\\bin\\MuseScore4.exe')
        ### add
        if flag:
            population = population[oril:]
        flag = False
        population = sorted(population, key=lambda x: x.score, reverse=True)
        best_performance = population[0].score
        if best_performance > criteria:
            break
        iter += 1
        print(population[0].score)
        ns.show('musicxml', app = r'C:\\Program Files\\MuseScore 4\\bin\\MuseScore4.exe')

            

    print("Generic Algorithms done.")
    stream_list = []
    # for i in range(10):
    #    stream_list.append(population[i].stream)
    stream_list.append(population[0].stream)
    return stream_list
