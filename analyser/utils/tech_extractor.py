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
    # Single-letter languages that must not be followed by symbols like ++ or #
    # \u2019 is the Unicode character for a right single quotation mark, which can appear in some contexts (e.g., "C’" instead of "C#").
    _SYMBOL_SUFFIXES = {"C": r"\b(?!(\+\+|#|'|\u2019))", "R": r'\b(?!\.)'}

    found = []
    for tech in _load_keywords():
        prefix = r'\b'
        suffix = _SYMBOL_SUFFIXES.get(tech, r'\b')
        pattern = prefix + re.escape(tech) + suffix
        match = re.search(pattern, text)
        if match:
            # Find the sentence containing the match
            start = text.rfind('.', 0, match.start())
            end = text.find('.', match.end())
            sentence = text[start + 1 : end + 1 if end != -1 else len(text)].strip()
            # print(f"[{tech}] -> \"{sentence}\"")
            found.append(tech)
    return found
