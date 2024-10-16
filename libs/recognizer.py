import whisper
import warnings
import os

model = None
def init_ai(model_name):
    global model
    # 初始化 Whisper 模型
    if model_name in whisper.available_models():
        print(f"加载模型: {model_name}")
        warnings.filterwarnings("ignore", category=FutureWarning)
        model = whisper.load_model(model_name)  # 你可以选择 'base', 'small', 'medium', 'large' 等不同模型
        print(f"模型加载完成！{model.device}")
    else:
        print(f"无效模型: {model_name}")
        print(f"可用模型: {whisper.available_models()}")
        os.exit(1)

def recognize_and_rename_audio(audio_file_path):
    """使用 Whisper 模型识别音频内容，并返回第一个单词"""
    result = model.transcribe(audio_file_path, fp16=False)
    # 获取识别的文本内容
    text = result['text'].strip()
    text = text.lower()
    text = ''.join([c for c in text if c.isalnum() or c.isspace()])
    if not text: return
    if len(result['segments']) == 0: return
    avg_logprob = result['segments'][0]['avg_logprob']
    no_speech_prob = result['segments'][0]['no_speech_prob']
    if avg_logprob < -1.5:
        # print(f"Skip Text: {text}  avg_logprob: {avg_logprob}")
        return

    if no_speech_prob > 0.45:
        # print(f"Skip Text: {text}  no_speech_prob: {no_speech_prob}")
        return
    # print(f"识别结果: {text} (avg_logprob: {avg_logprob}, no_speech_prob: {no_speech_prob})")
    return text