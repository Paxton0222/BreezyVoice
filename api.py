# OpenAI API Spec. Reference: https://platform.openai.com/docs/api-reference/audio/createSpeech

from contextlib import asynccontextmanager
from io import BytesIO

import torchaudio
from fastapi import FastAPI, Request, Body, Form
from fastapi.responses import StreamingResponse
from g2pw import G2PWConverter
from pydantic import BaseModel, Field
from pydantic_settings import BaseSettings

from cosyvoice.utils.file_utils import load_wav
from single_inference import CustomCosyVoice, get_bopomofo_rare


class Settings(BaseSettings):
    api_key: str = Field(
        default="", description="Specifies the API key used to authenticate the user."
    )

    model_path: str = Field(
        default="MediaTek-Research/BreezyVoice",
        description="Specifies the model used for speech synthesis.",
    )
    speaker_prompt_audio_path: str = Field(
        default="./data/佑希-新聞播報-ai.wav",
        # default="./data/laravel.wav",
        description="Specifies the path to the prompt speech audio file of the speaker.",
    )
    speaker_prompt_text_transcription: str = Field(
        default="以下是今天的新聞播報，美國蘋果公司在今天發表了新的 iPhone 17 系列，分別有 iPhone 17、iPhone 17 Plus、iPhone 17 Pro 和 iPhone 17 Pro Max，此次發表會還發表了全新升級的 AI 功能，讓 iPhone 17 系列有了比 siri 更加強大且實用的 AI 能力。",
        # default="今天我們從使用者發出請求開始，沿著 Laravel 的請求生命週期，一路走訪專案結構：從路由，Middleware，Controller，到商業邏輯，資料層與視圖，幫你建立一張清晰的心智地圖。",
        description="Specifies the transcription of the speaker prompt audio.",
    )


class SpeechRequest(BaseModel):
    model: str = ""
    input: str = Field(
        description="The content that will be synthesized into speech. You can include phonetic symbols if needed, though they should be used sparingly.",
        examples=["今天天氣真好"],
    )
    response_format: str = ""
    speed: float = 1.0


@asynccontextmanager
async def lifespan(app: FastAPI):
    app.state.settings = Settings()
    app.state.cosyvoice = CustomCosyVoice(app.state.settings.model_path)
    app.state.bopomofo_converter = G2PWConverter()
    app.state.prompt_speech_16k = load_wav(
        app.state.settings.speaker_prompt_audio_path, 16000
    )
    yield
    del app.state.cosyvoice
    del app.state.bopomofo_converter


app = FastAPI(lifespan=lifespan, root_path="/v1")


@app.get("/models")
async def get_models(request: Request):
    return {
        "object": "list",
        "data": [
            {
                "id": request.app.state.settings.model_path,
                "object": "model",
                "created": 0,
                "owned_by": "local",
            }
        ],
    }


@app.post("/audio/speech")
async def speach_endpoint(request: Request, input: str = Form(...)):
    # normalization
    speaker_prompt_text_transcription = (
        request.app.state.cosyvoice.frontend.text_normalize_new(
            request.app.state.settings.speaker_prompt_text_transcription, split=False
        )
    )
    content_to_synthesize = request.app.state.cosyvoice.frontend.text_normalize_new(
        input, split=False
    )
    speaker_prompt_text_transcription_bopomo = get_bopomofo_rare(
        speaker_prompt_text_transcription, request.app.state.bopomofo_converter
    )

    content_to_synthesize_bopomo = get_bopomofo_rare(
        content_to_synthesize, request.app.state.bopomofo_converter
    )
    output = request.app.state.cosyvoice.inference_zero_shot_no_normalize(
        content_to_synthesize_bopomo,
        speaker_prompt_text_transcription_bopomo,
        request.app.state.prompt_speech_16k,
    )
    audio_buffer = BytesIO()
    torchaudio.save(audio_buffer, output["tts_speech"], 22050, format="wav")
    audio_buffer.seek(0)
    return StreamingResponse(
        audio_buffer,
        media_type="audio/wav",
        headers={"Content-Disposition": "attachment; filename=output.wav"},
    )


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("api:app", host="0.0.0.0", port=8080)
