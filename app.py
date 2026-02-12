import streamlit as st
from collections import OrderedDict
import io

st.set_page_config(page_title="Vocabulary Organizer", page_icon="📚")

st.title("Vocabulary Cleaner & Organizer")

st.write("""
Paste your raw text. The app will:
- Remove duplicates
- Show unique lines
- Let you add optional language tags or notes
- Export clean vocabulary file
""")

text_input = st.text_area("Raw text here:", height=300)

if st.button("Process"):
    if text_input.strip() == "":
        st.warning("Please paste some text.")
    else:
        lines = [line.strip() for line in text_input.split("\n") if line.strip()]
        unique_lines = list(OrderedDict.fromkeys(lines))

        st.success(f"{len(unique_lines)} unique lines.")

        organized = []

        st.markdown("## Add optional language/notes")

        for i, line in enumerate(unique_lines):
            col1, col2, col3 = st.columns([3,1,2])

            with col1:
                st.write(f"**{line}**")

            with col2:
                lang = st.selectbox(
                    "Language",
                    ["", "DE", "EN", "PT"],
                    key=f"lang_{i}"
                )

            with col3:
                note = st.text_input(f"Notes (optional)", key=f"note_{i}")

            organized.append((line, lang, note))

        # Export
        output = io.StringIO()
        for original, lang, note in organized:
            line_out = original
            if lang:
                line_out += f" | {lang}"
            if note:
                line_out += f" | {note}"
            output.write(line_out + "\n")

        st.download_button(
            label="Download TXT file",
            data=output.getvalue(),
            file_name="vocabulary_output.txt",
            mime="text/plain"
        )
