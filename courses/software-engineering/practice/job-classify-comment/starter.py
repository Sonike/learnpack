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
    # TODO 1: a known label before the first ":" decides it
    # TODO 2: a comment ending in "?" is a question
    # TODO 3: a praise word makes it praise
    # TODO 4: anything else is blocking
    return "blocking"


if __name__ == "__main__":
    for c in ["nit: extra blank line here", "What happens if items is empty?",
              "Love how small this function is!", "This query is open to SQL injection."]:
        print(classify_comment(c), "<-", c)
