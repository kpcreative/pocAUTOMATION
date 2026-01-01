import re

def normalize_text(text: str) -> str:
    """
    Converts any text into a canonical comparable form.
    - lowercase
    - removes digits
    - removes special chars
    - removes spaces
    """
    if not text:
        return ""

    text = text.lower()
    text = re.sub(r"[0-9]", "", text)          # remove digits
    text = re.sub(r"[^a-z]", "", text)         # keep only letters
    return text
