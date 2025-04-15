import streamlit as st
import fitz  # PyMuPDF
from transformers import pipeline
import os

# --- Set Streamlit page config ---
st.set_page_config(page_title="Legal Document Analyzer", page_icon=":scroll:", layout="wide")

# --- Add logo ---
logo_url = "https://raw.githubusercontent.com/Yoshitach10/LegalAnalyzerApp/main/logo.png"
st.image(logo_url, width=150)

# --- Title ---
st.title("Legal Document Analyzer")
st.write("Upload a legal document (PDF) to extract and analyze its contents.")

# --- File upload with size check (limit: 5 MB) ---
uploaded_file = st.file_uploader("Upload your PDF file", type="pdf")

MAX_FILE_SIZE_MB = 5

def is_file_too_large(file):
    file.seek(0, os.SEEK_END)
    size_mb = file.tell() / (1024 * 1024)
    file.seek(0)
    return size_mb > MAX_FILE_SIZE_MB

if uploaded_file:
    if is_file_too_large(uploaded_file):
        st.warning("File too large! Please upload a PDF smaller than 5 MB.")
    else:
        # --- Extract text ---
        doc = fitz.open(stream=uploaded_file.read(), filetype="pdf")
        text = ""
        for page in doc:
            text += page.get_text()

        st.subheader("Extracted Text")
        st.text_area("Raw Text", text[:3000] + "..." if len(text) > 3000 else text, height=300)

        # --- Summarization (with safe truncation) ---
        if st.button("Summarize"):
            with st.spinner("Summarizing..."):
                summarizer = pipeline("summarization", model="sshleifer/distilbart-cnn-12-6")
                chunk = text[:1024]  # Process first 1024 characters only
                summary = summarizer(chunk, max_length=150, min_length=40, do_sample=False)[0]['summary_text']
                st.subheader("Summary")
                st.success(summary)

# --- Footer ---
st.markdown(
    """
    <hr style="margin-top: 30px; margin-bottom: 10px;">
    <div style="text-align: center;">
        <small>Created by Yoshita Chebrolu & Teammate • 2025</small>
    </div>
    """,
    unsafe_allow_html=True
)