import math
import os
import re
from collections import Counter
from uuid import uuid4

import docx2txt
import pdfplumber
from django.conf import settings
from django.core.files.storage import FileSystemStorage
from django.http import JsonResponse
from django.middleware.csrf import get_token
from django.shortcuts import render
from django.utils.text import get_valid_filename
from django.views.decorators.csrf import csrf_protect
from django.views.decorators.http import require_POST

from .utils.linkedin_parser import parse_linkedin_job_posting

ALLOWED_EXTENSIONS = {".pdf", ".docx"}
MAX_UPLOAD_SIZE_BYTES = 5 * 1024 * 1024  # 5 MB


def index(request):
    return render(request, "index.html")


def csrf_token_view(request):
    return JsonResponse({"csrfToken": get_token(request)})


def extract_text_from_pdf(pdf_path):
    text = ""
    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            extracted = page.extract_text() or ""
            text += extracted + "\n"
    return text.strip()


def extract_text_from_doc(docx_path):
    return (docx2txt.process(docx_path) or "").strip()


def _extension_from_name(filename):
    return os.path.splitext(filename)[1].lower()


def _save_upload(uploaded_file):
    ext = _extension_from_name(uploaded_file.name)
    if ext not in ALLOWED_EXTENSIONS:
        raise ValueError("Unsupported file type. Please upload a PDF or DOCX file.")

    if uploaded_file.size > MAX_UPLOAD_SIZE_BYTES:
        raise ValueError("File too large. Maximum allowed size is 5 MB.")

    storage = FileSystemStorage(
        location=os.path.join(settings.MEDIA_ROOT, "resumes"),
        base_url=os.path.join(settings.MEDIA_URL, "resumes/"),
    )
    os.makedirs(storage.location, exist_ok=True)

    safe_name = get_valid_filename(uploaded_file.name)
    filename = storage.save(f"{uuid4().hex}_{safe_name}", uploaded_file)
    return storage, filename, ext


def _tokenize(text):
    return re.findall(r"[A-Za-z0-9]+", text.lower())


def _tfidf_vectors(job_tokens, resume_tokens):
    docs = [job_tokens, resume_tokens]
    vocab = set(job_tokens) | set(resume_tokens)
    N = 2
    df = {term: sum(1 for doc in docs if term in doc) for term in vocab}

    def vector(tokens):
        if not tokens:
            return []
        tf = Counter(tokens)
        length = len(tokens)
        vec = []
        for term in vocab:
            idf = math.log((N + 1) / (df[term] + 1)) + 1
            vec.append((tf.get(term, 0) / length) * idf)
        return vec

    return vector(job_tokens), vector(resume_tokens)


def _cosine_similarity(vec_a, vec_b):
    if not vec_a or not vec_b:
        return 0.0
    dot = sum(a * b for a, b in zip(vec_a, vec_b))
    norm_a = math.sqrt(sum(a * a for a in vec_a))
    norm_b = math.sqrt(sum(b * b for b in vec_b))
    if norm_a == 0 or norm_b == 0:
        return 0.0
    return dot / (norm_a * norm_b)


def _calculate_match_score(resume_text, job_description):
    job_tokens = _tokenize(job_description)
    resume_tokens = _tokenize(resume_text)
    if not job_tokens or not resume_tokens:
        return 0.0
    job_vec, resume_vec = _tfidf_vectors(job_tokens, resume_tokens)
    similarity = _cosine_similarity(job_vec, resume_vec)
    return round(similarity * 100, 2)


def _extract_matched_terms(resume_text, job_description, top_n=8):
    resume_tokens = set(_tokenize(resume_text))
    job_tokens = _tokenize(job_description)
    seen = set()
    matches = []
    for token in job_tokens:
        if token in resume_tokens and token not in seen:
            matches.append(token)
            seen.add(token)
        if len(matches) >= top_n:
            break
    return matches


def _parse_job_data(job_url):
    job_data = parse_linkedin_job_posting(job_url)
    if not job_data:
        raise ValueError("Unable to parse job posting. Please verify the URL.")

    required_keys = {"job_title", "company_name", "job_location", "job_description"}
    if not required_keys.issubset(job_data):
        raise ValueError("Job posting is missing required fields.")

    return job_data


@require_POST
@csrf_protect
def match_requirements(request):
    uploaded_file = request.FILES.get("resume") or request.FILES.get("file")
    job_url = request.POST.get("job") or request.POST.get("job_url")

    if not uploaded_file or not job_url:
        return JsonResponse({"error": "Resume file and job URL are required."}, status=400)

    try:
        storage, filename, ext = _save_upload(uploaded_file)
    except ValueError as exc:
        return JsonResponse({"error": str(exc)}, status=400)

    file_path = storage.path(filename)
    try:
        if ext == ".pdf":
            resume_text = extract_text_from_pdf(file_path)
        else:
            resume_text = extract_text_from_doc(file_path)
    except Exception:
        storage.delete(filename)
        return JsonResponse({"error": "Could not read the uploaded resume."}, status=400)

    storage.delete(filename)

    try:
        job_data = _parse_job_data(job_url)
    except ValueError as exc:
        return JsonResponse({"error": str(exc)}, status=400)

    job_description = job_data.get("job_description", "")
    score = _calculate_match_score(resume_text, job_description) if job_description else 0
    matched_terms = _extract_matched_terms(resume_text, job_description)

    result = {
        "resume_text": resume_text[:200],
        "job_title": job_data["job_title"],
        "company": job_data["company_name"],
        "location": job_data["job_location"],
        "description": job_description[:500],
        "match_score": score,
        "matched_terms": matched_terms,
    }

    return JsonResponse(result)
