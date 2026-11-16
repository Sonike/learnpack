import re

CRITERIA_WORDS = ("given", "when", "then", "and")


def _is_criterion(line: str) -> bool:
    words = line.split()
    return bool(words) and words[0].lower() in CRITERIA_WORDS


def _part(pattern: str, line: str) -> str | None:
    match = re.search(pattern, line, re.IGNORECASE)
    if not match:
        return None
    return match.group(1).strip(" ,.") or None


def parse_user_story(text: str) -> dict:
    """Split a ticket into role, goal, benefit and acceptance criteria.

    Returns {"role", "goal", "benefit", "criteria", "missing"}.
    """
    lines = [line.strip() for line in text.splitlines() if line.strip()]
    criteria = [line for line in lines if _is_criterion(line)]
    story = next((line for line in lines if not _is_criterion(line)), "")

    result = {
        "role": _part(r"^as an? (.+?)(?:,|\bi want\b|$)", story),
        "goal": _part(r"\bi want (?:to )?(.+?)(?:,|\bso that\b|$)", story),
        "benefit": _part(r"\bso that (.+)$", story),
        "criteria": criteria,
    }
    result["missing"] = [name for name in ("role", "goal", "benefit", "criteria") if not result[name]]
    return result
