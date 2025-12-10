import shutil
import tempfile
from unittest.mock import patch

from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import Client, TestCase, override_settings

from analyser import views


class ExtractTextTests(TestCase):
    @patch("analyser.views.pdfplumber.open")
    def test_extract_text_from_pdf_handles_missing_page_text(self, mock_open):
        class DummyPage:
            def __init__(self, text):
                self._text = text

            def extract_text(self):
                return self._text

        class DummyPdf:
            def __init__(self, pages):
                self.pages = pages

            def __enter__(self):
                return self

            def __exit__(self, exc_type, exc_val, exc_tb):
                return False

        mock_open.return_value = DummyPdf([DummyPage(None), DummyPage("Hello world")])

        extracted = views.extract_text_from_pdf("fake.pdf")
        self.assertEqual(extracted, "Hello world")

    @patch("analyser.views.docx2txt.process")
    def test_extract_text_from_doc_strips_whitespace(self, mock_process):
        mock_process.return_value = "   Skills: Python, Django   \n"
        extracted = views.extract_text_from_doc("fake.docx")
        self.assertEqual(extracted, "Skills: Python, Django")


class MatchRequirementsTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.temp_dir = tempfile.mkdtemp()
        self.override_media = override_settings(MEDIA_ROOT=self.temp_dir)
        self.override_media.enable()
        self.addCleanup(self.override_media.disable)
        self.addCleanup(lambda: shutil.rmtree(self.temp_dir, ignore_errors=True))

    @patch("analyser.views.parse_linkedin_job_posting")
    @patch("analyser.views.extract_text_from_pdf")
    def test_match_requirements_success(self, mock_extract, mock_parse):
        mock_extract.return_value = "Python Django"
        mock_parse.return_value = {
            "job_title": "Backend Engineer",
            "company_name": "ACME",
            "job_location": "Remote",
            "job_description": "Python developer with Django experience",
        }

        pdf_file = SimpleUploadedFile("resume.pdf", b"%PDF-1.4 test", content_type="application/pdf")
        response = self.client.post(
            "/match_requirements",
            {"job": "http://example.com", "resume": pdf_file},
        )

        self.assertEqual(response.status_code, 200)
        payload = response.json()
        self.assertIn("match_score", payload)
        self.assertEqual(payload["job_title"], "Backend Engineer")
        self.assertIn("python", [term.lower() for term in payload.get("matched_terms", [])])

    def test_match_requirements_rejects_invalid_extension(self):
        bad_file = SimpleUploadedFile("resume.txt", b"text content", content_type="text/plain")
        response = self.client.post(
            "/match_requirements",
            {"job": "http://example.com", "resume": bad_file},
        )
        self.assertEqual(response.status_code, 400)
        self.assertIn("Unsupported file type", response.json()["error"])

    @patch("analyser.views.parse_linkedin_job_posting")
    @patch("analyser.views.extract_text_from_pdf")
    def test_match_requirements_handles_failed_job_parse(self, mock_extract, mock_parse):
        mock_extract.return_value = "Python Django"
        mock_parse.return_value = None

        pdf_file = SimpleUploadedFile("resume.pdf", b"%PDF-1.4 test", content_type="application/pdf")
        response = self.client.post(
            "/match_requirements",
            {"job": "http://example.com", "resume": pdf_file},
        )

        self.assertEqual(response.status_code, 400)
        self.assertIn("Unable to parse job posting", response.json()["error"])
