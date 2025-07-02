from transformers import MBartForConditionalGeneration, MBartTokenizer

# Загрузка модели один раз при старте
model_name = "facebook/mbart-large-50-many-to-many-mmt"
tokenizer = MBartTokenizer.from_pretrained(model_name)
model = MBartForConditionalGeneration.from_pretrained(model_name)

def translate_text(input_text: str, src_lang: str, tgt_lang: str) -> str:
    tokenizer.src_lang = src_lang
    encoded_input = tokenizer(input_text, return_tensors="pt", padding=True, truncation=True)
    generated_tokens = model.generate(**encoded_input, forced_bos_token_id=tokenizer.lang_code_to_id[tgt_lang])
    translated_text = tokenizer.batch_decode(generated_tokens, skip_special_tokens=True)[0]
    return translated_text
