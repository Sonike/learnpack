import re

AWS_KEY = re.compile(r"AKIA[0-9A-Z]{16}")
SK_KEY = re.compile(r"sk-[A-Za-z0-9_-]{20,}")
CODE_ASSIGNMENT = re.compile(
    r"(password|secret|api_key|token)\w*[\"']?\s*[=:]\s*(\"[^\"]+\"|'[^']+')",
    re.IGNORECASE,
)
ENV_LINE = re.compile(r"[A-Z0-9_]*(PASSWORD|SECRET|TOKEN|API_KEY)[A-Z0-9_]*=\S+")

PATTERNS = (AWS_KEY, SK_KEY, CODE_ASSIGNMENT)


def find_secrets(text: str) -> list[int]:
    """Return 1-based line numbers of lines that look like they contain a secret."""
    flagged = []
    for number, line in enumerate(text.splitlines(), start=1):
        if any(p.search(line) for p in PATTERNS) or ENV_LINE.fullmatch(line.strip()):
            flagged.append(number)
    return flagged
