import re
import os

_KEYWORDS_FILE = os.path.join(os.path.dirname(__file__), "tech_keywords.txt")


def _load_keywords():
    keywords = []
    with open(_KEYWORDS_FILE, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if line and not line.startswith("#"):
                keywords.append(line)
    return keywords


def extract_tech_stack(text):
    """
    Extracts technology keywords from a given text using a curated keyword list.
    Returns a sorted list of matched technologies (label preserved from the keyword list).
    """
    found = []
    for tech in _load_keywords():
        pattern = r'\b' + re.escape(tech) + r'\b'
        if re.search(pattern, text, re.IGNORECASE):
            found.append(tech)
    return found
