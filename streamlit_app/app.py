import streamlit as st
import requests

st.set_page_config(page_title="Переводчик", layout="centered")

st.title("🌍 Мультиязычный переводчик (Streamlit + FastAPI)")
st.write("Интерфейс: Streamlit, перевод выполняется через FastAPI + модель mBART")

# Инициализация session_state
if "translated_text" not in st.session_state:
    st.session_state.translated_text = ""
if "reversed_text" not in st.session_state:
    st.session_state.reversed_text = ""

# Ввод исходного текста
input_text = st.text_area("Введите текст для перевода:")

# Выбор языков
col1, col2 = st.columns(2)
with col1:
    src_lang = st.selectbox("Исходный язык", ["en_XX", "ru_RU", "fr_XX", "de_DE", "es_XX"])
with col2:
    tgt_lang = st.selectbox("Целевой язык", ["en_XX", "ru_RU", "fr_XX", "de_DE", "es_XX"])

# Кнопка перевода
if st.button("Перевести"):
    if input_text.strip():
        try:
            response = requests.post("http://localhost:8000/translate", json={
                "text": input_text,
                "source_lang": src_lang,
                "target_lang": tgt_lang
            })
            if response.status_code == 200:
                st.session_state.translated_text = response.json()["translated_text"]
                st.session_state.reversed_text = ""
            else:
                st.error("Ошибка при обращении к API.")
        except Exception as e:
            st.error(f"Не удалось подключиться к серверу FastAPI: {e}")
    else:
        st.warning("Пожалуйста, введите текст для перевода.")

# Отображение перевода
if st.session_state.translated_text:
    st.markdown("#### ✅ Перевод:")
    st.success(st.session_state.translated_text)

    # Кнопка обратного перевода
    if st.button("Обратный перевод"):
        try:
            rev_response = requests.post("http://localhost:8000/translate", json={
                "text": st.session_state.translated_text,
                "source_lang": tgt_lang,
                "target_lang": src_lang
            })
            if rev_response.status_code == 200:
                st.session_state.reversed_text = rev_response.json()["translated_text"]
            else:
                st.error("Ошибка при обратном переводе.")
        except Exception as e:
            st.error(f"Ошибка соединения с API: {e}")

# Отображение обратного перевода
if st.session_state.reversed_text:
    st.markdown("#### 🔁 Обратный перевод:")
    st.info(st.session_state.reversed_text)
