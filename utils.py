from PyPDF2 import PdfReader
import os

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


# 📄 Extract text from PDF
def extract_text_from_pdf(file_path):
    if not os.path.exists(file_path):
        raise Exception("File not found")

    if os.path.getsize(file_path) == 0:
        raise Exception("PDF file is empty")

    reader = PdfReader(file_path)
    text = ""

    for page in reader.pages:
        page_text = page.extract_text()
        if page_text:
            text += page_text

    return text


# 🧠 Lightweight text preprocessing (NO spaCy)
def preprocess(text):
    text = text.lower()
    words = text.split()

    # basic stop words
    stop_words = {
        "the", "is", "in", "and", "to", "of", "a", "for",
        "on", "with", "as", "by", "an", "be", "this", "that"
    }

    words = [
        word for word in words
        if word.isalpha() and word not in stop_words
    ]

    return " ".join(words)


# 📊 Similarity using TF-IDF
def semantic_similarity(resume, jd):
    vectorizer = TfidfVectorizer()

    vectors = vectorizer.fit_transform([resume, jd])

    score = cosine_similarity(vectors[0:1], vectors[1:2]) # type: ignore

    return round(score[0][0] * 100, 2)