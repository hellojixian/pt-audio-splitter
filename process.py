#!/usr/bin/env python
from pydub import AudioSegment
from pydub.silence import detect_silence, split_on_silence
import os
import whisper

# 定义每次加载的最大时间块大小（例如5分钟的块，300秒 = 300000毫秒）
chunk_duration = 60000 * 5  # 最大5分钟的音频块
chunk_nearset_silence = 5000  # 5秒内的静音位置
# 创建文件夹存储片段
project_folder = os.path.dirname(__file__)
audio = AudioSegment.from_wav(f"{project_folder}/source/raw_audio_1.wav")
output_folder = f"{project_folder}/output_segments"

os.makedirs(output_folder, exist_ok=True)
# delete all existing files in the output folder
for file in os.listdir(output_folder):
    os.remove(os.path.join(output_folder, file))

# 初始化 Whisper 模型
model = whisper.load_model("base")  # 你可以选择 'base', 'small', 'medium', 'large' 等不同模型

def find_nearest_silence(audio_chunk, start_time, chunk_duration, silence_thresh=-40, min_silence_len=300):
    """找到临近静音的位置以便调整块的结束位置"""
    # 查找这个范围内的静音位置，检测结果返回的是 [(start, end), ...] 的列表
    silence_ranges = detect_silence(audio_chunk, min_silence_len=min_silence_len, silence_thresh=silence_thresh)

    # 在当前块的末尾附近查找一个静音点
    for silence_start, silence_end in silence_ranges:
        # 找到第一个接近块末尾的静音位置，允许静音起点在 (chunk_duration - 1秒) 到 (chunk_duration + 1秒) 内
        if chunk_duration - chunk_nearset_silence  <= silence_start <= chunk_duration + chunk_nearset_silence:
            return start_time + silence_start  # 返回相对于原始音频的时间点

    # 如果没有找到合适的静音位置，返回原来的块结束位置
    return start_time + chunk_duration

def recognize_and_rename_audio(audio_file_path):
    """使用 Whisper 模型识别音频内容，并返回第一个单词"""
    result = model.transcribe(audio_file_path)
    # 获取识别的文本内容
    print(result)
    text = result['text'].strip()
    text = text.lower()
    # remove punctuations from text but keep the spaces
    text = ''.join([c for c in text if c.isalnum() or c.isspace()])
    return text

def process_audio_chunk(audio_chunk, chunk_index=0, silence_thresh=-40, min_silence_len=500):
    global word_index
    # 使用 pydub 的 split_on_silence 函数，基于静音分割音频
    segments = split_on_silence(
        audio_chunk,
        min_silence_len=min_silence_len,  # 最短的静音间隔长度 (毫秒)
        silence_thresh=silence_thresh,  # 静音的阈值（音量低于此值被认为是静音）
        keep_silence=200  # 保留一些静音部分 (这里设置为200ms)
    )

    # 保存音频片段并使用 Whisper 识别内容
    for i, segment in enumerate(segments):
        segment_file = f"{output_folder}/segment_{chunk_index}_{i + 1}.wav"
        segment.export(segment_file, format="wav")
        print(f"导出文件: {segment_file}")

        # 识别该音频片段中的内容
        recognized_word = recognize_and_rename_audio(segment_file)

        # 使用识别到的第一个单词重新命名音频文件
        new_file_name = f"{output_folder}/{word_index}_{recognized_word}.wav"
        os.rename(segment_file, new_file_name)
        print(f"重命名为: {new_file_name}")
        word_index += 1

# 加载大文件
total_duration = len(audio)  # 获取总长度（毫秒）

# 按块处理，寻找静音位置作为边界
chunk_index = 0
start_time = 0
word_index = 0
while start_time < total_duration:
    end_time = min(start_time + chunk_duration, total_duration)

    # 从当前时间开始找到最近的静音点来调整块的结束位置
    adjusted_end_time = find_nearest_silence(audio[start_time:end_time], start_time, chunk_duration)

    # 如果找到的结束时间比之前的块要长，则更新为新的块结束时间
    audio_chunk = audio[start_time:adjusted_end_time]

    # 处理这个音频块
    process_audio_chunk(audio_chunk, chunk_index=chunk_index)

    # 更新下一个块的起始时间
    start_time = adjusted_end_time
    chunk_index += 1

print("音频处理完成！")
