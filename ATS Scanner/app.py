import streamlit as st
import google.generativeai as genai
import os
import PyPDF2 as pdf
import json
from dotenv import load_dotenv

load_dotenv()             # Load all environment variables

genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))


#    Generating Response from the Gemini Pro Model
def get_gemini_response(input):
    model=genai.GenerativeModel("gemini-pro")
    response=model.generate_content(input)
    return response.text


#    Converting PDF to Text
def input_pdf_text(uploaded_file):
    reader=pdf.PdfReader(uploaded_file)
    text=""
    for page in range(len(reader.pages)):
        page =reader.pages[page]
        text +=str(page.extract_text())
    return text

# Generating Prompt Template
input_prompt="""
Act like a skilled or experienced application tracking system(ATS).
With a deep understanding of Tech field(Software Engineering, Data Analyst/Scientist, Machine Learning, Big Data)
Your task is to evaluate the resume based on the given Job Description.
You must consider the job market is very competitive and you must provide the assistance for improving the resume.
Also assign the percentage match based on the Job Description(JD) and the missing keywords with high accuracy.

resume : {text} 
description:{JD}

I want response in a single line in the form of string having structure 
{{"JD Match" : "%", 
"Missing Keywords :[]",
"Profile Summary":""}}


"""

# Streamlit App
st.title("Smart ATS")
st.text("Improve Your Resume ATS")
jd=st.text_area("Paste the Job Description")
uploaded_file=st.file_uploader("upload your resume",type="pdf",help="Upload the document in PDf only")
submit=st.button('Submit')

if submit:
    if uploaded_file is not None:
        text=input_pdf_text(uploaded_file)
        response = get_gemini_response(input_prompt)
        st.subheader(response)








