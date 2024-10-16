from pydub import AudioSegment
from pydub.silence import detect_silence, split_on_silence
import os

# 创建文件夹存储片段
project_folder = os.path.dirname(os.path.dirname(__file__))
output_segments_folder = f"{project_folder}/output_segments"
output_folder = f"{project_folder}/output_words"

chunk_nearset_silence = 5000  # 5秒内的静音位置
word_index = 0

def init_folders():
    os.makedirs(output_segments_folder, exist_ok=True)
    for file in os.listdir(output_segments_folder):
        os.remove(os.path.join(output_segments_folder, file))

    os.makedirs(output_folder, exist_ok=True)
    for file in os.listdir(output_folder):
        os.remove(os.path.join(output_folder, file))

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

def process_audio_chunk(audio_chunk, progress_bar=None, silence_thresh=-40, min_silence_len=500, cb=None):
    global word_index
    # 使用 pydub 的 split_on_silence 函数，基于静音分割音频
    segments = split_on_silence(
        audio_chunk,
        min_silence_len=min_silence_len,  # 最短的静音间隔长度 (毫秒)
        silence_thresh=silence_thresh,  # 静音的阈值（音量低于此值被认为是静音）
        keep_silence=200  # 保留一些静音部分 (这里设置为200ms)
    )

    # 保存音频片段并使用 Whisper 识别内容
    for _, segment in enumerate(segments):
        segment_file = f"{output_segments_folder}/segment_{word_index}.wav"
        segment.export(segment_file, format="wav")

        # 识别该音频片段中的内容
        recognized_word = cb(segment_file)

        # 使用识别到的第一个单词重新命名音频文件
        if recognized_word:
            recognized_word = recognized_word.replace(" ", "-")
            new_file_name = f"{output_folder}/{str(word_index).zfill(4)}_{recognized_word}.wav"
            os.rename(segment_file, new_file_name)
            # print(f"重命名为: {new_file_name}")
            word_index += 1

        # 更新进度条，假设每个 segment 的长度为音频片段的一部分
        if progress_bar:
            progress_bar.update(len(segment)/1000)  # 更新进度条，增加处理的音频长度
