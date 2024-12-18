import os



# 把一个音符（形式如music.txt）映射到21-108的某个数中（对应钢琴上的88个键）
def musical_note_to_map(note):
    note_dict = {'a': 0, 'b': 2, 'c': 3, 'd': 5, 'e': 7, 'f': 8, 'g': 10}
    bias = 0
    if note[0]=='#':
        bias = 1
    if note[0+bias] not in note_dict:
        return -1
    
    else:
        num = int(note[1+bias])
        if (note[0+bias]!='a') & (note[0+bias]!='b'):
            num = num-1
        value = note_dict[note[0+bias]] + num*12 +21
    if (value+bias<21) | (value+bias)>108:
        print(note)
        print('value error')
        return -1
    return value+bias

# 把一行旋律（形式如music.txt）转换成list[int]
def music_to_vector(melody):
    v = []
    for i in range(len(melody)-1):
        note = melody[i]
        if note ==' ':
            continue
        elif note[0] =='-':
            v.append(20) 
            continue
        elif note[0] == '0':
            v.append(0)
            continue
        else:
            ret = musical_note_to_map(note)
            if ret==-1:
                continue
            v.append(ret)
    
    if len(v) != 32:
        print('current:',melody)
        print(len(v))
        print('wrong len of melody')
        exit(1)
    
    return (v, melody[32].strip())

# 把music.txt中的所有转成向量的旋律一起放到一个向量里（现在另外更新了16首旋律，一共是31首旋律
# 包含的调号有A a a# C c D d F# f#，但是感觉并不是随便找点歌来就能执行算法的，总之看后续效果再改
def musicTxt_to_vector():
    v_list = []
    # 为了后续排查数据问题，这里还是分成两份，新数据没有合并
    with open('music_data/music.txt') as file:
        contents = file.readlines()
        for line in contents:
            melody = line.split(' ')

            v = music_to_vector(melody)
            v_list.append(v)
    with open('music_data/music2.txt') as file:
        contents = file.readlines()
        for line in contents:

            melody = line.split(' ')

            v = music_to_vector(melody)
            v_list.append(v)


    return v_list

