import streamlit as st
import spacy
from PyPDF2 import PdfReader

# Load English NLP model
nlp = spacy.load("en_core_web_sm")

# --- Function to extract text from PDF ---
def extract_text_from_pdf(uploaded_file):
    pdf_reader = PdfReader(uploaded_file)
    text = ""
    for page in pdf_reader.pages:
        text += page.extract_text()
    return text

# --- Function to analyze resume ---
def analyze_resume(text, job_description):
    doc = nlp(text.lower())
    jd_doc = nlp(job_description.lower())

    # Extract keywords (nouns + proper nouns)
    resume_keywords = set([token.text for token in doc if token.pos_ in ["NOUN", "PROPN"]])
    jd_keywords = set([token.text for token in jd_doc if token.pos_ in ["NOUN", "PROPN"]])

    # Keyword match percentage
    matched = resume_keywords.intersection(jd_keywords)
    match_percent = round(len(matched) / len(jd_keywords) * 100, 2) if jd_keywords else 0

    return match_percent, matched, jd_keywords

# --- Streamlit UI ---
st.title("📄 AI Resume Analyzer")
st.write("Upload your resume and compare it with a job description to check ATS compatibility.")

uploaded_file = st.file_uploader("Upload Resume (PDF)", type=["pdf"])
job_description = st.text_area("Paste Job Description Here")

if uploaded_file and job_description:
    text = extract_text_from_pdf(uploaded_file)
    match_percent, matched, jd_keywords = analyze_resume(text, job_description)

    st.subheader("Analysis Result")
    st.write(f"✅ Match Score: **{match_percent}%**")
    st.write(f"🔑 Matched Keywords: {', '.join(matched)}")
    st.write(f"📌 Job Description Keywords: {', '.join(jd_keywords)}")
