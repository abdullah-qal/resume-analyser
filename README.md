# Resume Analyser

Analyze a CV (PDF/DOCX) against a LinkedIn job posting using Django and a Vite/React interface

# Prerequisites :
Python 3.11+ 
Node.js 18+ and npm

# Backend Installation
Create a virtual environment and activate it and install the dependencies:

```bash
python -m pip install -r requirements.txt

```
Apply the migrations and start the server:

```bash
python manage.py migrate
python manage.py runserver 8000

```

# Frontend Installation
In `resume_analyser_frontend`, install the dependencies:

```bash
cd resume_analyser_frontend
npm install

```
Start the dev server quickly:

```bash
npm run dev
```

The interface listens on `http://localhost:5173` and calls the Django API on `http://localhost:8000`

# Useful Endpoints
- `GET /csrf/`: returns a CSRF token and sets the `csrftoken` cookie for front-end requests.

- `POST /match_requirements`: expeccts `resume` (PDF/DOCX file, ≤ 5 MB) and `job` (LinkedIn URL). It responds with a resume excerpt, job posting information, a TF-IDF score 0-100, and matching keywords.

# Security and CORS
- CSRF enabled front-end sends `X-CSRFToken` and `credentials: include`

- CORS limited to `http://localhost:5173` with credentials support.

- The files are temporarily stored under `MEDIA_ROOT/resumes` and then deleted after being read.

# Tests
Run the Django suite:
```bash
python manage.py test
``` The tests mock the LinkedIn call and extractors to avoid network calls and reading real binary documents