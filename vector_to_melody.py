import os


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