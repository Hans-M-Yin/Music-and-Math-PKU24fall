from music21 import *
from music_to_vector import *
from vector_to_melody import *
from generic_algs import *
import subprocess
import os
from ly_process import *
 

def generate_png(style):
    
    print("translating melody to vector...")
    vecs = musicTxt_to_vector(style)

    melodies = []
    for i in range(0, len(vecs)):
        melodies.append(vector_to_stream(vecs[i][0], vecs[i][1]))

    print("running generic algorithm...")
    s = run_generic_algorithm(melodies)

    print("writing lilypond files...")
    for index, ss in enumerate(s):
        lilypond_file_path = f'output_{index + 1}.ly'
        ss.write('lilypond', fp=lilypond_file_path)

    print("processing .ly files...")
    directory_path = os.path.dirname(os.path.abspath(__file__))
    process_directory(directory_path)

    for index, ss in enumerate(s):
        lilypond_file_path = f'output_{index + 1}.ly'
        # 使用 LilyPond 生成乐谱图片
        print("running lilypond...")
        # 如果没有添加环境变量需要修改路径

        # process = subprocess.run(
        #             [r'/usr/bin/lilypond', '--png',  lilypond_file_path],
        #             capture_output=True, text=True, encoding='utf-8'  # 添加 encoding 参数
        #         )
        
        process = subprocess.run(
                    [r'lilypond', '--png',  lilypond_file_path],
                    capture_output=True, text=True, encoding='utf-8'  # 添加 encoding 参数
                    )

        if process.returncode != 0:
            print(f"LilyPond 命令执行失败，文件: {lilypond_file_path}")

    print("所有乐谱图片已生成。")

# if __name__ == "__main__":
#     generate_png()