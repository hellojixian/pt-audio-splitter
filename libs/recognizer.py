import whisper

# 初始化 Whisper 模型
print("加载模型...")
model = whisper.load_model("base")  # 你可以选择 'base', 'small', 'medium', 'large' 等不同模型
print("模型加载完成！")

def recognize_and_rename_audio(audio_file_path):
    """使用 Whisper 模型识别音频内容，并返回第一个单词"""
    result = model.transcribe(audio_file_path, fp16=False)
    # 获取识别的文本内容
    text = result['text'].strip()
    text = text.lower()
    # remove punctuations from text but keep the spaces
    text = ''.join([c for c in text if c.isalnum() or c.isspace()])
    return text