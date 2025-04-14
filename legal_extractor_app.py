import streamlit as st
import fitz  # PyMuPDF
import re
import os
import openai
from transformers import pipeline
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# Load OpenAI API key
openai.api_key = st.secrets["OPENAI_API_KEY"] if "OPENAI_API_KEY" in st.secrets else os.getenv("OPENAI_API_KEY")

# Utility: Extract text from PDF
def extract_text_from_pdf(uploaded_file):
    with fitz.open(stream=uploaded_file.read(), filetype="pdf") as doc:
        return "\n".join([page.get_text() for page in doc])

# Module 2: Summarization
def summarize_text(text):
    summarizer = pipeline("summarization", model="sshleifer/distilbart-cnn-12-6")
    chunks = [text[i:i+1000] for i in range(0, len(text), 1000)]
    return " ".join([summarizer(chunk)[0]["summary_text"] for chunk in chunks])

# Module 3: Clause Extraction
def extract_clauses(text):
    return re.findall(r'(Clause\s\d+[:\s].*?)(?=\nClause\s\d+:|\Z)', text, re.DOTALL)

# Module 4: Risk Identification
def identify_risky_clauses(clauses, risky_keywords):
    risky = []
    for clause in clauses:
        if any(keyword.lower() in clause.lower() for keyword in risky_keywords):
            risky.append(clause)
    return risky

# Module 5: Clause Comparison
def compare_clause_similarity(clause, reference_clause):
    vectorizer = TfidfVectorizer().fit_transform([clause, reference_clause])
    similarity = cosine_similarity(vectorizer[0:1], vectorizer[1:2])
    return similarity[0][0]

# Module 6: AI-based Clause Rewriting
def rewrite_clause_with_ai(clause):
    prompt = f"Rewrite the following legal clause in a clearer, more standard form:\n\n\"{clause}\""
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": prompt}],
        max_tokens=200,
        temperature=0.7
    )
    return response["choices"][0]["message"]["content"].strip()

# Streamlit App UI
st.set_page_config(page_title="Legal Document Analyzer", layout="wide")
st.title("📚 AI-Powered Legal Document Analyzer")

uploaded_file = st.file_uploader("Upload a legal PDF document", type=["pdf"])

if uploaded_file:
    raw_text = extract_text_from_pdf(uploaded_file)
    st.subheader("📄 Extracted Text")
    with st.expander("View extracted text"):
        st.write(raw_text)

    # Summarization
    if st.button("Summarize Document"):
        with st.spinner("Summarizing..."):
            summary = summarize_text(raw_text)
        st.subheader("📝 Summary")
        st.write(summary)

    # Clause Extraction
    if st.button("Extract Clauses"):
        clauses = extract_clauses(raw_text)
        st.subheader("📜 Extracted Clauses")
        for idx, clause in enumerate(clauses, 1):
            st.markdown(f"**Clause {idx}:** {clause}")

    # Risk Identification
    if st.button("Identify Risky Clauses"):
        risky_keywords = ["terminate", "penalty", "breach", "liability", "indemnify", "damages"]
        clauses = extract_clauses(raw_text)
        risky = identify_risky_clauses(clauses, risky_keywords)
        st.subheader("⚠️ Risky Clauses")
        if risky:
            for clause in risky:
                st.warning(clause)
        else:
            st.success("No risky clauses identified.")

    # Clause Comparison
    st.subheader("📊 Compare a Clause")
    user_clause = st.text_area("Paste a clause to compare")
    reference_clause = st.text_area("Paste the reference clause")
    if st.button("Compare Clauses"):
        if user_clause and reference_clause:
            similarity = compare_clause_similarity(user_clause, reference_clause)
            st.info(f"Similarity score: **{similarity:.2f}**")
        else:
            st.error("Please enter both clauses.")

    # Clause Rewriting
    st.subheader("✍️ AI Clause Rewriting")
    clause_to_rewrite = st.text_area("Enter a clause you'd like to rewrite")
    if st.button("Rewrite Clause"):
        if clause_to_rewrite:
            rewritten = rewrite_clause_with_ai(clause_to_rewrite)
            st.success("✅ Rewritten Clause")
            st.write(rewritten)
        else:
            st.error("Please enter a clause to rewrite.")
