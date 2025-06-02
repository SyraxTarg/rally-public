import os
import re
from dotenv import load_dotenv

load_dotenv()

BANNED_WORDS = set()

def load_banned_words():
    """used to load the bad words from the txt file."""
    global BANNED_WORDS
    with open(os.getenv("BANNED_TERMS_PATH"), "r", encoding="utf-8") as f:
        BANNED_WORDS = set(word.strip().lower() for word in f)

def is_content_clean(content: str) -> bool:
    """used to check if the given content is free of bad words."""
    content_lower = content.lower()
    words = re.findall(r'\b\w+\b', content_lower)
    return not any(word in BANNED_WORDS for word in words)

load_banned_words()
