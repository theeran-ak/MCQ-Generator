import os
from PyPDF2 import PdfReader
import PyPDF2
import json
import traceback
from langchain_community.document_loaders import PyPDFLoader


def read_file(uploaded_file):
    if uploaded_file is not None:
        if uploaded_file.type == "application/pdf":
            # Read PDF
            pdf_reader = PdfReader(uploaded_file)
            text = ""
            for page in pdf_reader.pages:
                text += page.extract_text() or ""  # Avoid None if page has no text
            #st.text_area("Extracted Text", text, height=300)

        elif uploaded_file.type == "text/plain":
            # Read TXT
            text = uploaded_file.read().decode("utf-8")
        return text
def get_table_data(quiz_str):
    try:
        data=json.loads(quiz_str)

# convert to df
        rows = []
        for qid, content in data.items():
            if qid.isdigit():  # skip 'review'
                mcq = content['mcq']
                choices = " | ".join([f"{k}: {v}" for k, v in content['options'].items()])
                correct = content['correct']
                rows.append({"mcq": mcq, "choices": choices, "correct": correct})

        return rows
        
    except Exception as e:
        traceback.print_exception(type(e), e, e.__traceback__)
        return False