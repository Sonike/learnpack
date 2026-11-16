import re

LABELS = {
    "nit": "nit",
    "nitpick": "nit",
    "question": "question",
    "praise": "praise",
    "kudos": "praise",
    "blocking": "blocking",
    "issue": "blocking",
    "must": "blocking",
}
PRAISE_WORDS = {"nice", "great", "love", "thanks", "thank", "clean", "neat"}


def classify_comment(text: str) -> str:
    """Return "blocking", "nit", "question" or "praise" for a review comment."""
    if ":" in text:
        label = text.split(":", 1)[0].strip().lower()
        if label in LABELS:
            return LABELS[label]
    if text.strip().endswith("?"):
        return "question"
    words = set(re.findall(r"[a-z]+", text.lower()))
    if words & PRAISE_WORDS:
        return "praise"
    return "blocking"
