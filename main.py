from music21 import *
from music_to_vector import *
from vector_to_melody import *
from generic_algs import *
import subprocess
from music21 import stream, note, midi
from midi2audio import FluidSynth
import os
from ly_process import *


def generate_png(style):

    print("translating melody to vector...")
    vecs = musicTxt_to_vector(style)

    melodies = []
    for i in range(0, len(vecs)):
        melodies.append(vector_to_stream(vecs[i][0], vecs[i][1]))

    print("running generic algorithm...")
    s = run_generic_algorithm(melodies, total=1)

    print("writing lilypond files...")
    for index, ss in enumerate(s):
        midi_file_path = 'output.mid'
        mf = midi.translate.music21ObjectToMidiFile(ss)
        mf.open(midi_file_path, 'wb')
        mf.write()
        mf.close()


        # 创建 FluidSynth 实例，指定 SoundFont 文件
        fluidsynth_path = 'FluidSynth/bin/fluidsynth.exe'  # 替换为你的 FluidSynth 路径
        soundfont_path = 'FluidSynth/soundfont.sf2'  # 替换为你的 SoundFont 路径
        print(f"FluidSynth 路径: {fluidsynth_path}")
        # 创建 FluidSynth 实例，指定 FluidSynth 路径和 SoundFont 文件
        fs = FluidSynth(soundfont_path)

        # 指定 MIDI 文件和输出 WAV 文件的路径
        midi_file_path = 'output.mid'
        wav_file_path = 'output_audio.wav'

        # 转换 MIDI 为 WAV
        fs.midi_to_audio(midi_file_path, wav_file_path)

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
