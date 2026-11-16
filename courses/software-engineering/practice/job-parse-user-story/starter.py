import re

CRITERIA_WORDS = ("given", "when", "then", "and")


def parse_user_story(text: str) -> dict:
    """Split a ticket into role, goal, benefit and acceptance criteria.

    Returns {"role", "goal", "benefit", "criteria", "missing"}.
    """
    # TODO: find the criteria lines (they start with Given/When/Then/And)
    # TODO: find the story line (first non-blank line that isn't a criterion)
    # TODO: pull out role, goal and benefit with re.search(..., re.IGNORECASE)
    # TODO: list the missing parts in order: role, goal, benefit, criteria
    return {"role": None, "goal": None, "benefit": None, "criteria": [], "missing": []}


if __name__ == "__main__":
    ticket = """As a library member, I want to renew a loan online so that I don't pay late fees.

Given I have a book due tomorrow
When I click "Renew"
Then the due date moves forward 14 days"""
    print(parse_user_story(ticket))
    print(parse_user_story("Make the button blue"))
