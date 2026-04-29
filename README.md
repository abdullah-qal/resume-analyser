# resume-analyser

## Running the Project

### Backend (Django)

```bash
# From the project root
.\venv\Scripts\Activate.ps1
python manage.py migrate
python manage.py runserver
```

### Frontend (React/Vite)

```bash
.\venv\Scripts\Activate.ps1
cd resume_analyser_frontend
npm install
npm run dev
```

Run both simultaneously — the Django backend runs on `http://localhost:8000` and the Vite dev server on `http://localhost:5173`.
