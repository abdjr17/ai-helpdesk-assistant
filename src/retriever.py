"""Finds the guides that match a user's question.

No AI is used here. We just count how many important words from the question
appear in each guide. Words in the title and in the "Keywords:" line count more.
"""
import re
from pathlib import Path

GUIDES_DIR = Path(__file__).resolve().parent.parent / "guides"

# Words that carry no meaning for matching.
STOPWORDS = {
    "a", "an", "the", "is", "are", "was", "were", "be", "do", "does", "did", "i", "my",
    "me", "we", "you", "your", "it", "its", "to", "of", "in", "on", "at", "for", "and",
    "or", "not", "no", "can", "cannot", "how", "what", "why", "when", "where", "this",
    "that", "with", "from", "have", "has", "had", "get", "got", "need", "please", "help",
    "after", "before", "keeps", "today", "very", "new", "up", "out", "if", "so", "but",
    "there", "they", "them", "us", "our", "any", "some", "should", "would", "could",
    "company", "work", "working",
}

MIN_SCORE = 3  # below this score we say "no guide found"


def tokenize(text):
    """Lowercase the text, split it into words, drop stopwords, cut plural 's'."""
    words = re.findall(r"[a-zäöüß0-9]+", text.lower())
    cleaned = []
    for w in words:
        if w in STOPWORDS or len(w) < 2:
            continue
        if len(w) > 3 and w.endswith("s"):
            w = w[:-1]
        if len(w) > 5 and w.endswith("ed"):
            w = w[:-2]
        elif len(w) > 6 and w.endswith("ing"):
            w = w[:-3]
        cleaned.append(w)
    return cleaned


def load_guides():
    """Read every .md file in the guides folder."""
    guides = []
    for path in sorted(GUIDES_DIR.glob("*.md")):
        text = path.read_text(encoding="utf-8")
        lines = text.splitlines()
        title = lines[0].lstrip("# ").strip()
        keywords_line = next((l for l in lines if l.lower().startswith("keywords:")), "")
        keywords = keywords_line.split(":", 1)[1] if keywords_line else ""
        guides.append({
            "id": path.stem,
            "title": title,
            "text": text,
            "title_words": set(tokenize(title)),
            "keyword_words": set(tokenize(keywords)),
            "body_words": set(tokenize(text)),
        })
    return guides


def retrieve(question, guides, top_k=2):
    """Return up to top_k guides with their scores, best first."""
    q_words = set(tokenize(question))
    scored = []
    for g in guides:
        score = 0
        score += 3 * len(q_words & g["title_words"])
        score += 3 * len(q_words & g["keyword_words"])
        score += 1 * len(q_words & g["body_words"])
        if score >= MIN_SCORE:
            scored.append((score, g))
    scored.sort(key=lambda x: x[0], reverse=True)
    return [(g, s) for s, g in scored[:top_k]]
