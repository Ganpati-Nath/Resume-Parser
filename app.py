import streamlit as st
import json
from PyPDF2 import PdfReader

# Set Streamlit page configuration
st.set_page_config(page_title="Resume Parser", page_icon="📄", layout="wide")

# Custom CSS for improved UI and animations
st.markdown(
    """
    <style>
    .main {
        background-color: #857e7e;
        background-image: linear-gradient(160deg, #857e7e 0%, #4e9487 33%, #857e7e 66%, #857e7e 100%);

        padding: 20px;
        border-radius: 10px;
    }
    .title {
        font-family: 'Arial Black', sans-serif;
        color: #000000;
    }
    .subheader {
        font-family: 'Arial', sans-serif;
        color: #000000;
    }
    .upload-box {
        border: 2px dashed #2E86C1;
        padding: 20px;
        border-radius: 10px;
        background-color: #ffffff;
        transition: transform 0.3s ease-in-out;
    }
    .upload-box:hover {
        transform: scale(1.05);
    }
    .stButton>button {
        background-color: #2E86C1;
        color: #ffffff;
        border: none;
        border-radius: 5px;
        padding: 10px 20px;
        transition: background-color 0.3s ease-in-out, transform 0.3s ease-in-out;
    }
    .stButton>button:hover {
        background-color: #1B4F72;
        transform: scale(1.05);
    }
    .json-box {
        background-color: #ffffff;
        padding: 20px;
        border-radius: 10px;
        border: 1px solid #2E86C1;
        transition: transform 0.3s ease-in-out;
    }
    .json-box:hover {
        transform: scale(1.02);
    }
    .download-button {
        margin-top: 20px;
    }
    .stTextArea {
        color: #000000 !important;
    }
    .footer {
        font-family: 'Arial', sans-serif;
        color: #000000;
        text-align: center;
        margin-top: 50px;
        padding-top: 20px;
        border-top: 1px solid #000000;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# Function to parse resume content
def parse_resume(file):
    pdf_reader = PdfReader(file)
    resume_text = ""
    for page in pdf_reader.pages:
        resume_text += page.extract_text()
    return resume_text

# Function to convert resume text to JSON
def convert_to_json(resume_text):
    # Sample parsing logic - you can enhance this based on the resume format
    resume_lines = resume_text.split('\n')
    resume_json = {
        "name": resume_lines[0],
        "contact": resume_lines[1],
        "email": resume_lines[2],
        "experience": [line for line in resume_lines[3:] if "experience" in line.lower()],
        "education": [line for line in resume_lines[3:] if "education" in line.lower()],
        "skills": [line for line in resume_lines[3:] if "skills" in line.lower()]
    }
    return resume_json

# Streamlit application
st.markdown('<h1 class="title">Resume Parser</h1>', unsafe_allow_html=True)
st.markdown('<h3 class="subheader">Upload your resume (PDF format) and get a structured JSON output</h3>', unsafe_allow_html=True)
uploaded_file = st.file_uploader("", type="pdf", label_visibility="collapsed")

if uploaded_file is not None:
    with st.spinner('Parsing your resume...'):
        resume_text = parse_resume(uploaded_file)
        resume_json = convert_to_json(resume_text)

    st.markdown('<h3 class="subheader">Parsed Resume Content</h3>', unsafe_allow_html=True)
    st.markdown('<div class="json-box">', unsafe_allow_html=True)
    st.json(resume_json)
    st.markdown('</div>', unsafe_allow_html=True)

    # Option to download JSON
    json_data = json.dumps(resume_json, indent=4)
    st.download_button(label="Download JSON", data=json_data, file_name="resume.json", mime="application/json")

    # Optional: Display the raw text of the resume
    if st.checkbox("Show raw resume text"):
        st.text_area("Raw Resume Text", resume_text, height=300)

# Footer
st.markdown(
    '<div class="footer">Copyright © 2024 | Resume Parser | Ganpati Nath | NATH.dev | All Rights Reserved.</div>',
    unsafe_allow_html=True
)
