import streamlit as st
from langdetect import detect
from collections import OrderedDict
from googletrans import Translator
import io

st.set_page_config(page_title="Free Auto Translator", page_icon="📚")

st.title("Free Auto Translation Vocabulary Organizer")

translator = Translator()

def detect_language(text):
    try:
        lang = detect(text)
        if lang in ["de", "en", "pt"]:
            return lang
        else:
            return "other"
    except:
        return "unknown"

text_input = st.text_area("Paste text here:", height=300)

target_lang = st.selectbox(
    "Translate all lines to:",
    ["en (English)", "pt (Portuguese)", "de (German)"]
)

if st.button("Process Text"):
    if text_input.strip() == "":
        st.warning("Please paste some text!")
    else:
        lines = [line.strip() for line in text_input.split("\n") if line.strip()]
        unique_lines = list(OrderedDict.fromkeys(lines))

        st.success(f"{len(unique_lines)} unique lines found.")

        results = []

        for line in unique_lines:
            detected = detect_language(line)

            try:
                translated = translator.translate(line, dest=target_lang.split()[0])
                translation_text = translated.text
            except Exception as e:
                translation_text = f"[error] {str(e)}"

            st.write(f"**{line}** ({detected}) → {translation_text}")

            results.append((line, translation_text))

        # EXPORT FILE
        output = io.StringIO()
        for original, translation in results:
            output.write(f"{original} — {translation}\n")

        st.download_button(
            label="Download TXT file",
            data=output.getvalue(),
            file_name="vocabulary_output.txt",
            mime="text/plain"
        )
