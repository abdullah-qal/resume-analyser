from django.shortcuts import render
from django.core.files.storage import FileSystemStorage
from django.http import HttpResponse
import pdfplumber  # For extracting text from PDFs
import os

from django.shortcuts import render

def index(request):
    return render(request, 'index.html')

def extract_text_from_pdf(pdf_path):
    """Extracts text from a PDF file."""
    text = ""
    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            text += page.extract_text() + "\n"
    return text.strip()

def upload_resume(request):
    if request.method == 'POST' and request.FILES.get('file'):
        uploaded_file = request.FILES['file']
        
        if not uploaded_file.name.endswith('.pdf'):
            return HttpResponse("Please upload a valid PDF file.", status=400)
        
        fs = FileSystemStorage()
        filename = fs.save(uploaded_file.name, uploaded_file)
        file_path = fs.path(filename)

        # Extract text from the PDF
        extracted_text = extract_text_from_pdf(file_path)

        # Do something with the extracted text (e.g., store in DB, process it, etc.)
        print(extracted_text)  # Debugging: Prints extracted text

        return HttpResponse(f"File uploaded and processed successfully. Extracted text: {extracted_text[:200]}...")  # Show first 200 chars
     
    return HttpResponse("Something went wrong", status=500)
