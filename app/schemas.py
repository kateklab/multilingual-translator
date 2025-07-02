from pydantic import BaseModel
from pydantic import BaseModel, validator


class TranslationRequest(BaseModel):
    text: str
    source_lang: str
    target_lang: str

    @validator('text')
    def text_must_not_be_empty(cls, v):
        if not v.strip():
            raise ValueError('Text must not be empty')
        return v

class TranslationResponse(BaseModel):
    translated_text: str
