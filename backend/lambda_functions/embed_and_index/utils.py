import re

def clean_text(text: str) -> str:
    """
    Normalize and clean raw text. 
    """
    text = re.sub(r"https?://\S+|www\.\S+", "", text)
    text = re.sub(r"<.*?>", "", text)
    text = re.sub(r"\s+", " ", text)
    return text.strip()

def chunk_text(text: str, chunk_size: int = 256) -> list:
    """
    Split cleaned text into sequential chunks of up to `chunk_size` words.
    Returns a list of text chunks.
    """
    words = text.split()
    if not words:
        return []

    chunks = []
    for i in range(0, len(words), chunk_size):
        chunk = words[i:i + chunk_size]
        chunks.append(" ".join(chunk))
    return chunks
