import streamlit as st
from langdetect import detect
from collections import OrderedDict
import io

st.set_page_config(page_title="Vocabulary Organizer", layout="wide")

st.title("Vocabulary Organizer (DE / EN / PT)")

st.write("Paste your raw text below. The app will remove duplicates and allow manual translations.")

# Input area
text_input = st.text_area("Paste text here:", height=300)

def detect_language(text):
    try:
        lang = detect(text)
        if lang in ["de", "en", "pt"]:
            return lang
        else:
            return "unknown"
    except:
        return "unknown"

if st.button("Process Text"):
    if text_input.strip() == "":
        st.warning("Please paste some text.")
    else:
        lines = [line.strip() for line in text_input.split("\n") if line.strip()]
        unique_lines = list(OrderedDict.fromkeys(lines))

        st.success(f"{len(unique_lines)} unique lines found.")

        results = []

        st.markdown("## Add Translations Manually")

        for i, line in enumerate(unique_lines):
            lang = detect_language(line)

            col1, col2, col3 = st.columns([2,1,2])

            with col1:
                st.write(f"**{line}**")

            with col2:
                st.write(f"Detected: `{lang}`")

            with col3:
                translation = st.text_input(
                    f"Translation for line {i}",
                    key=f"trans_{i}"
                )

            results.append((line, translation))

        # Export
        if st.button("Export as TXT"):
            output = io.StringIO()

            for original, translation in results:
                if translation:
                    output.write(f"{original} — {translation}\n")
                else:
                    output.write(f"{original}\n")

            st.download_button(
                label="Download file",
                data=output.getvalue(),
                file_name="vocabulary_output.txt",
                mime="text/plain"
            )
