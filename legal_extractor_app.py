import streamlit as st
import fitz  # PyMuPDF
from transformers import pipeline

st.title("AI-Powered Legal Document Analyzer")

uploaded_file = st.file_uploader("Upload a legal document (PDF)", type="pdf")

if uploaded_file:
    with fitz.open(stream=uploaded_file.read(), filetype="pdf") as doc:
        text = ""
        for page in doc:
            text += page.get_text()
    
    st.subheader("Extracted Text")
    st.text_area("Full Document Text", text, height=300)

    # Summarize the text
    summarizer = pipeline("summarization", model="sshleifer/distilbart-cnn-12-6")
    summary = summarizer(text, max_length=150, min_length=40, do_sample=False)[0]['summary_text']

    st.subheader("Summarized Text")
    st.write(summary)
