from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_translate():
    payload = {
        "text": "Hello",
        "source_lang": "en_XX",
        "target_lang": "ru_RU"
    }
    response = client.post("/translate", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert "translated_text" in data
    assert isinstance(data["translated_text"], str)
    assert len(data["translated_text"]) > 0

def test_reverse_translate():
    # Сначала переводим с английского на русский
    payload_forward = {
        "text": "Hello",
        "source_lang": "en_XX",
        "target_lang": "ru_RU"
    }
    response_forward = client.post("/translate", json=payload_forward)
    assert response_forward.status_code == 200
    translated_text = response_forward.json()["translated_text"]
    assert len(translated_text) > 0

    # Затем обратный перевод с русского на английский
    payload_reverse = {
        "text": translated_text,
        "source_lang": "ru_RU",
        "target_lang": "en_XX"
    }
    response_reverse = client.post("/translate", json=payload_reverse)
    assert response_reverse.status_code == 200
    reversed_text = response_reverse.json()["translated_text"]
    assert isinstance(reversed_text, str)
    assert len(reversed_text) > 0
def test_translate_empty_text():
    # Тестируем запрос с пустым текстом
    response = client.post("/translate", json={
        "text": "",
        "source_lang": "en_XX",
        "target_lang": "ru_RU"
    })
    # Можно ожидать, что сервер вернёт ошибку валидации или пустой перевод
    assert response.status_code == 422 or response.status_code == 400

def test_translate_missing_fields():
    # Тестируем запрос без обязательных полей
    response = client.post("/translate", json={
        "source_lang": "en_XX"
        # "text" и "target_lang" отсутствуют
    })
    assert response.status_code == 422  # ошибка валидации
