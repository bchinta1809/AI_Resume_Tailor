from pypdf import PdfReader
import streamlit as st
from openai import OpenAI
from dotenv import load_dotenv
import os

load_dotenv()


client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY")
)
def extract_text_from_pdf(uploaded_file):
    reader = PdfReader(uploaded_file)
    text = ""

    for page in reader.pages:
        page_text = page.extract_text()
        if page_text:
            text += page_text + "\n"

    return text

st.title("🤖 AI Resume Tailor")
st.write("Optimize your resume for ATS systems using AI-powered analysis.")
uploaded_resume = st.file_uploader(
    "Upload Resume PDF",
    type=["pdf"],
    key="resume_pdf_uploader"
)
resume_text = st.text_area(
    "Or Paste Resume Text",
    height=400
)

resume = ""

if uploaded_resume is not None:
    st.success("Resume PDF uploaded successfully.")
    resume = extract_text_from_pdf(uploaded_resume)
else:
    resume = resume_textresume = ""

if uploaded_resume is not None:
    resume = extract_text_from_pdf(uploaded_resume)
else:
    resume = resume_text
job_desc = st.text_area(
    "Paste Job Description",
    height=250
)

if st.button("Analyze Resume"):

    if not resume.strip():
        st.warning("Please upload or paste your resume first.")
        st.stop()

    if not job_desc.strip():
        st.warning("Please paste the job description first.")
        st.stop()
with st.spinner("Analyzing resume..."):
    prompt = f"""
You are an ATS Resume Expert.

Resume:
{resume}
Job Description:
{job_desc}

Give:
1. ATS Match Score
2. Missing Skills
3. Resume Improvements
4. Tailored Resume Summary
"""
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {
                "role":"user",
                "content":prompt
            }
        ]
    )

    st.write(response.choices[0].message.content)