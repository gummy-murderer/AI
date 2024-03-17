import torch
from TTS.api import TTS
import os
from datetime import datetime

# Get device
device = "cuda" if torch.cuda.is_available() else "cpu"
# device = "cpu"

# List available 🐸TTS models
print(TTS().list_models())

# Init TTS
tts = TTS("tts_models/multilingual/multi-dataset/xtts_v2").to(device)

# 절대 경로
script_dir = os.path.dirname(os.path.abspath(__file__))
# 상대 경로
before_relative_path = r'tts_before\voice_hg.wav'
# 최종 절대 경로
before_abs_file_path = os.path.join(script_dir, before_relative_path)

def define_text_to_speech(text):
    print("TTS start")
    result_relative_path = r'tts_result'
    result_file_name = datetime.now().strftime("%Y%m%d_%H%M%S") + ".wav"
    result_abs_file_path = os.path.join(script_dir, result_relative_path, result_file_name)
    print("result_abs_file_path =", result_abs_file_path)
    tts.tts_to_file(text=text, 
                file_path=result_abs_file_path, 
                speaker_wav=before_abs_file_path, 
                language="ko")
    print("TTS finish")
    return result_file_name