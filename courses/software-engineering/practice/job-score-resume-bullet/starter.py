ACTION_VERBS = {
    "added", "automated", "built", "cut", "debugged", "deployed", "designed",
    "developed", "fixed", "implemented", "improved", "launched", "led",
    "migrated", "optimised", "optimized", "reduced", "refactored", "shipped",
    "sped", "tested", "wrote", "created", "integrated", "mentored",
}


def score_resume_bullet(text: str) -> list[str]:
    """Return the problems with one resume bullet, in a fixed order."""
    problems = []
    # TODO: strip spaces and a leading "-", "*" or "•"
    # TODO: check the four rules in order and append the exact problem strings
    return problems


if __name__ == "__main__":
    for b in ["- Built a FastAPI service with 14 endpoints and 92% test coverage",
              "Responsible for the backend of a group project",
              "Worked on tests"]:
        print(score_resume_bullet(b), "<-", b)
