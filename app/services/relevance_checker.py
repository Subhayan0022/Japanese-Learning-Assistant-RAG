import re
import pymupdf as fitz

SAMPLE_PAGES = 5
MIN_JAPANESE_CHARS = 50

JAPANESE_PATTERN = re.compile(
    r'[\u3040-\u309F'   # Hiragana
    r'\u30A0-\u30FF'    # Katakana
    r'\u4E00-\u9FFF]'   # Kanji
)


def extract_sample_text(pdf_bytes: bytes) -> str:
    doc = fitz.open(stream=pdf_bytes, filetype="pdf")
    text = ""
    for i in range(min(SAMPLE_PAGES, len(doc))):
        text += doc[i].get_text()
    doc.close()
    return text.strip()


def check_relevance(pdf_bytes: bytes, *args) -> tuple[bool, str]:
    sample_text = extract_sample_text(pdf_bytes)

    if not sample_text:
        return False, "Could not extract text from PDF."

    japanese_chars = JAPANESE_PATTERN.findall(sample_text)
    count = len(japanese_chars)

    print(f"Relevance check — Japanese character count: {count}")

    if count >= MIN_JAPANESE_CHARS:
        return True, "PDF is relevant to Japanese learning."
    else:
        return False, f"PDF does not appear to contain Japanese content (found {count} Japanese characters, need {MIN_JAPANESE_CHARS})."
