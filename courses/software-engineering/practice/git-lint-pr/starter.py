import re

SECTIONS = ["What", "Why", "How to test"]
MAX_LINES = 400


def lint_pr_description(md: str) -> list[str]:
    """Problems with a PR description: missing sections, no linked issue, too big."""
    problems = []
    # TODO: collect the heading names: lines like "## What" or "### how to test:"
    #       (re.findall(r"^#{1,6} +(.+?):?\s*$", md, re.MULTILINE) gives you the text after the #s)
    # TODO: for each name in SECTIONS that's missing (ignore case): "Missing section: <name>"
    # TODO: no "#<digits>" anywhere -> "No linked issue (add e.g. Closes #123)"
    # TODO: a "Size: N" line with N > MAX_LINES -> f"Too big: {N} changed lines (aim for under 400)"
    return problems


if __name__ == "__main__":
    print(lint_pr_description("Fixed stuff\n\nSize: 950"))
