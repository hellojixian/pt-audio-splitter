#!/usr/bin/env python
from pydub import AudioSegment
import os
from tqdm import tqdm
from .libs.spliter import find_nearest_silence, process_audio_chunk, init_folders
from .libs.recognizer import recognize_and_rename_audio

# 定义每次加载的最大时间块大小（例如5分钟的块，300秒 = 300000毫秒）
chunk_duration = 60000   # 最大1分钟的音频块

# 创建文件夹存储片段
project_folder = os.path.dirname(__file__)
audio = AudioSegment.from_wav(f"{project_folder}/source/raw_audio_1.wav")

# 加载大文件
total_duration = len(audio)  # 获取总长度（毫秒）
progress_bar = tqdm(total=total_duration/1000, unit='sec', desc='Processing Audio')

# 按块处理，寻找静音位置作为边界
chunk_index = 0
start_time = 0

init_folders()
while start_time < total_duration:
    end_time = min(start_time + chunk_duration, total_duration)

    # 从当前时间开始找到最近的静音点来调整块的结束位置
    adjusted_end_time = find_nearest_silence(audio[start_time:end_time], start_time, chunk_duration)

    # 如果找到的结束时间比之前的块要长，则更新为新的块结束时间
    audio_chunk = audio[start_time:adjusted_end_time]

    # 处理这个音频块并更新进度条
    process_audio_chunk(audio_chunk, progress_bar=progress_bar, cb=recognize_and_rename_audio)

    # 更新下一个块的起始时间
    start_time = adjusted_end_time
    chunk_index += 1

    progress_bar.update((adjusted_end_time - start_time)/1000)  # 更新外部循环的进度条

progress_bar.close()

print("音频处理完成！")