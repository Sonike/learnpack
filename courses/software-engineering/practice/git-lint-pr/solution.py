import re

SECTIONS = ["What", "Why", "How to test"]
MAX_LINES = 400


def lint_pr_description(md: str) -> list[str]:
    """Problems with a PR description: missing sections, no linked issue, too big."""
    problems = []

    headings = re.findall(r"^#{1,6} +(.+?):?\s*$", md, re.MULTILINE)
    found = {h.strip().lower() for h in headings}
    for section in SECTIONS:
        if section.lower() not in found:
            problems.append(f"Missing section: {section}")

    if not re.search(r"#\d+", md):
        problems.append("No linked issue (add e.g. Closes #123)")

    size = re.search(r"^size:\s*(\d+)", md, re.MULTILINE | re.IGNORECASE)
    if size and int(size.group(1)) > MAX_LINES:
        problems.append(f"Too big: {size.group(1)} changed lines (aim for under {MAX_LINES})")

    return problems
