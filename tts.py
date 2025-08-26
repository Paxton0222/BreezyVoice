from single_inference import CustomCosyVoice, G2PWConverter, get_bopomofo_rare
from cosyvoice.utils.file_utils import load_wav
from transformers import pipeline
import torchaudio
import time

class TTS:
    def __init__(self, prompt_path: str, prompt_text: str):
        self.model = CustomCosyVoice("MediaTek-Research/BreezyVoice-300M")
        self.g2pw_converter = G2PWConverter()
        # 載入音訊檔案
        self.prompt_speech_16k = load_wav(prompt_path, 16000)
        # prompt 音訊檔文字
        self.speaker_prompt_text_transcription = self.model.frontend.text_normalize_new(
            prompt_text,
            split=False,
        )
        self.speaker_prompt_text_transcription_bopomo = get_bopomofo_rare(self.speaker_prompt_text_transcription, self.g2pw_converter)

    def generate(self, generate_text: str, output_path: str):
        
        # 生成文字
        content_to_synthesize = self.model.frontend.text_normalize_new(
            generate_text,
            split=False
        )
        content_to_synthesize_bopomo = get_bopomofo_rare(content_to_synthesize, self.g2pw_converter)
        # 生成語音
        start = time.time()
        output = self.model.inference_zero_shot_no_normalize(content_to_synthesize_bopomo, self.speaker_prompt_text_transcription_bopomo, self.prompt_speech_16k)
        end = time.time()
        torchaudio.save(output_path, output['tts_speech'], 22050)