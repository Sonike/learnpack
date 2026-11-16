ACTION_VERBS = {
    "added", "automated", "built", "cut", "debugged", "deployed", "designed",
    "developed", "fixed", "implemented", "improved", "launched", "led",
    "migrated", "optimised", "optimized", "reduced", "refactored", "shipped",
    "sped", "tested", "wrote", "created", "integrated", "mentored",
}


def score_resume_bullet(text: str) -> list[str]:
    """Return the problems with one resume bullet, in a fixed order."""
    bullet = text.strip().lstrip("-*•").strip()
    words = bullet.split()
    first = words[0].lower().strip(".,;:!") if words else ""

    problems = []
    if first not in ACTION_VERBS:
        problems.append("no action verb")
    if not any(ch.isdigit() for ch in bullet):
        problems.append("no number")
    if "responsible for" in bullet.lower():
        problems.append("responsible for")
    if len(bullet) > 200:
        problems.append("too long")
    return problems
