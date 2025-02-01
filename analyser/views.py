from django.shortcuts import render
from django.core.files.storage import FileSystemStorage
from django.http import HttpResponse
from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt

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
    uploaded_file = request.FILES['resume']
    
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
        job_url = request.POST.get('job')
        job_data = parse_linkedin_job_posting(job_url)
        return job_data
    
# NOTE: The CSRF exemption is only for development purposes. It needs to be handled properly.
@csrf_exempt
def match_requirements(request):
    if request.method != "POST":
        return JsonResponse({"error": "Invalid request method"}, status=405)
    
    resume_text = upload_resume(request)
    job_data = parse_job_posting(request)

    result = {
        "resume_text": f"Resume Text (first 200 chars): {resume_text[:200]}...<br><br>",
        "job_title": job_data['job_title'],
        "company": job_data['company_name'],
        "location": job_data['job_location'],
        "description": f"{job_data['job_description'][:40]}..."
    }

    return JsonResponse(result)


