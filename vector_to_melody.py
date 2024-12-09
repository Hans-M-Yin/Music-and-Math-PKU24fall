import os
from music_to_vector import *
from music21 import *

# 把21-108代表音符的数字重新转换成音符
def num_to_note(num):
    note_dict = {0: 'A', 1: 'A#', 2: 'B', 3: 'C', 4: 'C#', 5: 'D', 6: 'D#', 7: 'E', 8: 'F', 
                  9: 'F#', 10: 'G', 11: 'G#'}
    if (num < 21) | (num > 108):
        print("warning : wrong num")
        exit(1)
    num = num - 21
    alpha = num % 12  
    belta = num // 12 
    if alpha > 2:
        belta = belta + 1
    note_str = note_dict[alpha] + str(belta)
    return note_str


def vector_to_stream(vector:list[int]) -> stream:
    s = stream.Stream()
    current_length = 0
    current_type = -1
    prev_num = -1
    # current_type = 0 for rest
    # current_type = 1 for note
    flag = False
    for num in vector:
        if num == 0:
            if flag :
                if current_type == 0:
                    r = note.Rest(quarterLength = current_length / 2)
                    s.append(r)
                elif current_type == 1:
                    r = note.Note(num_to_note(prev_num), quarterLength = current_length / 2)
                    s.append(r)
            current_type = 0
            current_length = 1
            prev_num = num
            flag = True
        elif 21 <= num and num <= 108:
            if flag :
                if current_type == 0:
                    r = note.Rest(quarterLength = current_length / 2)
                    s.append(r)
                elif current_type == 1:
                    r = note.Note(num_to_note(prev_num), quarterLength = current_length / 2)
                    s.append(r)
            current_type = 1
            current_length = 1
            prev_num = num
            flag = True
        elif num == 20:
            current_length += 1

    if current_type == 0:
        r = note.Rest(quarterLength = current_length / 2)
        s.append(r)
    elif current_type == 1:
        r = note.Note(num_to_note(num), quarterLength = current_length / 2)
        s.append(r) 
    return s     

# 把向量重新转换成旋律
def vector_to_melody(vector):
    ret_str = []
    for num in vector:
        if num == 20:
            ret_str.append('-')
        elif num == 0:
            ret_str.append('0')
        else:
            word = num_to_note(num)
            ret_str.append(word)
    ret = ' '.join(ret_str)
    return ret