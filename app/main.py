from fastapi import FastAPI
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
import os

from app.model import translate_text
from app.schemas import TranslationRequest, TranslationResponse

app = FastAPI(title="Multilingual Translator")

# 📦 Эндпоинт API для перевода
@app.post("/translate", response_model=TranslationResponse)
def translate(req: TranslationRequest):
    translated = translate_text(req.text, req.source_lang, req.target_lang)
    return TranslationResponse(translated_text=translated)

# 🌐 Отдача index.html при переходе на корень
@app.get("/", response_class=FileResponse)
def read_index():
    return FileResponse(os.path.join("static", "index.html"))

# 📁 Подключение папки со статикой (если будут CSS/JS)
app.mount("/static", StaticFiles(directory="static"), name="static")
