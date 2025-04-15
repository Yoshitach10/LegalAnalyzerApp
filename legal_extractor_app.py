import streamlit as st
from PIL import Image
import fitz  # PyMuPDF
import re
import os
import openai
from transformers import pipeline
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# --- Streamlit Page Config ---
st.set_page_config(
    page_title="Legal Document Analyzer",
    page_icon="⚖️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- Logo ---
st.markdown(
    "<div style='text-align: center; margin-bottom: 1rem;'>"
    "<img src='https://raw.githubusercontent.com/Yoshitach10/LegalAnalyzerApp/main/logo.png' width='120'>"
    "</div>",
    unsafe_allow_html=True
)

# --- Load OpenAI Key ---
openai.api_key = st.secrets["OPENAI_API_KEY"] if "OPENAI_API_KEY" in st.secrets else os.getenv("OPENAI_API_KEY")

# --- PDF Text Extraction ---
def extract_text_from_pdf(uploaded_file):
    with fitz.open(stream=uploaded_file.read(), filetype="pdf") as doc:
        return "\n".join([page.get_text() for page in doc])

# --- Summarization ---
@st.cache_resource
def load_summarizer():
    return pipeline("summarization", model="sshleifer/distilbart-cnn-12-6")

summarizer = load_summarizer()

def summarize_text(text):
    chunks = [text[i:i+1000] for i in range(0, len(text), 1000)]
    results = []
    for chunk in chunks:
        summary = summarizer(chunk, max_length=130, min_length=30, do_sample=False)[0]['summary_text']
        results.append(summary)
    return " ".join(results)

# --- Clause Extraction ---
clause_keywords = {
    "Confidentiality": ["confidential", "non-disclosure", "privacy"],
    "Termination": ["terminate", "termination", "cancel", "end of agreement"],
    "Payment": ["payment", "compensation", "fee", "remuneration"],
    "Governing Law": ["jurisdiction", "governing law", "under the laws of"],
    "Indemnity": ["indemnify", "liability", "hold harmless"],
    "Force Majeure": ["force majeure", "act of god", "unforeseen circumstances"],
    "Dispute Resolution": ["arbitration", "dispute", "litigation", "settlement"]
}

def extract_clauses(text):
    extracted_clauses = {}
    sentences = re.split(r'(?<=[.!?]) +', text)
    for clause, keywords in clause_keywords.items():
        matched_sentences = [s.strip() for s in sentences if any(k.lower() in s.lower() for k in keywords)]
        if matched_sentences:
            extracted_clauses[clause] = matched_sentences
    return extracted_clauses

# --- Risk Detection ---
def find_risky_clauses(clauses, risky_keywords):
    risky = []
    for clause in clauses:
        if any(keyword.lower() in clause.lower() for keyword in risky_keywords):
            risky.append(clause)
    return risky

# --- Clause Comparison ---
standard_clauses = {
    "termination": "This agreement may be terminated by either party upon giving written notice of 30 days.",
    "liability": "The liability of the parties shall be limited to direct damages only.",
    "dispute_resolution": "Any disputes arising shall be resolved through arbitration in accordance with applicable laws.",
    "confidentiality": "Parties agree to maintain the confidentiality of shared information during and after the agreement term."
}

def compare_with_standard_clauses(clauses, standard_clauses):
    comparisons = []
    for clause in clauses:
        max_similarity = 0
        best_match = ""
        for label, standard in standard_clauses.items():
            vectorizer = TfidfVectorizer().fit_transform([clause, standard])
            similarity = cosine_similarity(vectorizer[0:1], vectorizer[1:2])
            if similarity[0][0] > max_similarity:
                max_similarity = similarity[0][0]
                best_match = standard
        comparisons.append((clause, best_match, round(max_similarity, 2)))
    return comparisons

# --- AI Clause Rewriting ---
def rewrite_clause_with_ai(clause):
    prompt = f"Rewrite the following legal clause in a clearer, more standard form:\n\n\"{clause}\""
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": prompt}],
        max_tokens=200,
        temperature=0.7
    )
    return response["choices"][0]["message"]["content"].strip()

# --- App Interface ---
st.title("📚 AI-Powered Legal Document Analyzer")
uploaded_file = st.file_uploader("Upload a legal PDF document", type=["pdf"])

if uploaded_file:
    raw_text = extract_text_from_pdf(uploaded_file)

    st.subheader("📄 Extracted Text")
    with st.expander("View extracted text"):
        st.write(raw_text)

    st.caption("📌 Summarization may take a few seconds for large files.")
    if st.button("Summarize Document"):
        with st.spinner("Summarizing your document..."):
            summary = summarize_text(raw_text)
        st.subheader("🧠 Summary")
        st.write(summary)

    if st.button("Extract Clauses"):
        clauses_dict = extract_clauses(raw_text)
        st.subheader("📜 Extracted Clauses")
        for title, lines in clauses_dict.items():
            st.markdown(f"### {title} Clause")
            for l in lines:
                st.write(f"- {l}")
        st.session_state["clauses"] = [c for sublist in clauses_dict.values() for c in sublist]

    if st.button("Identify Risky Clauses"):
        risky_keywords = ["terminate", "penalty", "breach", "liability", "indemnify", "damages"]
        clauses = st.session_state.get("clauses", [])
        risky = find_risky_clauses(clauses, risky_keywords)
        st.subheader("⚠️ Risky Clauses")
        if risky:
            for clause in risky:
                st.warning(clause)
            st.session_state["risky"] = risky
        else:
            st.success("No risky clauses identified.")

    st.subheader("📊 Compare a Clause")
    user_clause = st.text_area("Paste a clause to compare")
    reference_clause = st.text_area("Paste the reference clause")
    if st.button("Compare Clauses"):
        if user_clause and reference_clause:
            similarity = compare_with_standard_clauses([user_clause], {"ref": reference_clause})
            st.info(f"Similarity score: **{similarity[0][2]:.2f}**")
        else:
            st.error("Please enter both clauses.")

    st.subheader("✍️ AI Clause Rewriting")
    clause_to_rewrite = st.text_area("Enter a clause you'd like to rewrite")
    if st.button("Rewrite Clause"):
        if clause_to_rewrite:
            rewritten = rewrite_clause_with_ai(clause_to_rewrite)
            st.success("✅ Rewritten Clause")
            st.write(rewritten)
        else:
            st.error("Please enter a clause to rewrite.")
else:
    st.info("Please upload a PDF to begin.")

# --- Footer ---
st.markdown("---")
st.markdown(
    "<div style='text-align: center; font-size: 14px; color: gray;'>"
    "Developed by <strong>Yoshita Chebrolu</strong> and <strong>[Your Teammate's Name]</strong> 💻✨"
    "</div>",
    unsafe_allow_html=True
)