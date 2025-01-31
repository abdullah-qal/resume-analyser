from django.shortcuts import render
from django.core.files.storage import FileSystemStorage
from django.http import HttpResponse
from django.shortcuts import render
from .utils.linkedin_parser import parse_linkedin_job_posting

import docx2txt # For extracting text from DOCX files
import pdfplumber # For extracting text from PDFs
import os
"""Displays HTML front-end."""
def index(request):
    return render(request, 'index.html')

"""Extracting logic."""
def extract_text_from_pdf(pdf_path):
    text = ""
    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            text += page.extract_text() + "\n"
    return text.strip()

def extract_text_from_doc(docx_path):
    return docx2txt.process(docx_path).strip()


def get_file_type(file_path):
    ext = os.path.splitext(file_path)[1].lower() # Get the file extension
    match ext:
        case '.pdf':
            return 'pdf'
        case '.docx':
            return 'docx'
        case _:
            return None
        
"""Uploads a resume and extracts text from it."""
def upload_resume(request):
    uploaded_file = request.FILES['file']
    
    fs = FileSystemStorage()
    filename = fs.save(uploaded_file.name, uploaded_file)
    file_path = fs.path(filename)

    # Extract text from the PDF
    ext = get_file_type(file_path)
    if ext == 'pdf':
        extracted_text = extract_text_from_pdf(file_path)
    elif ext == 'docx':
        extracted_text = extract_text_from_doc(file_path)
    else:
        return "Invalid file type"
    return extracted_text

def parse_job_posting(request):
        job_url = request.POST.get('job_url')
        job_data = parse_linkedin_job_posting(job_url)
        return job_data

def match_requirements (request):
    if request.method == 'POST' and request.FILES.get('file'):

        resume_text = upload_resume(request)
        job_data = parse_job_posting(request)

        # Combine the results
        result = (
            f"Resume Text (first 200 chars): {resume_text[:200]}...<br><br>"
            f"Job Title: {job_data['job_title']}<br>"
            f"Company: {job_data['company_name']}<br>"
            f"Location: {job_data['job_location']}<br>"
            f"Description (first 200 chars): {job_data['job_description'][:200]}..."
        )

        # TODO Match the requirements between resume and job posting

        return HttpResponse(result)
    return HttpResponse("Invalid request or missing data.", status=400)

