from solution import parse_user_story

FULL = """As a library member, I want to renew a loan online so that I don't pay late fees.

Given I have a book due tomorrow
When I click "Renew"
Then the due date moves forward 14 days
And I see a confirmation message"""


def test_extracts_role_goal_and_benefit():
    got = parse_user_story(FULL)
    want = ("library member", "renew a loan online", "I don't pay late fees")
    assert (got["role"], got["goal"], got["benefit"]) == want, f"expected {want!r}, got {(got['role'], got['goal'], got['benefit'])!r}"


def test_collects_criteria_lines_in_order():
    got = parse_user_story(FULL)["criteria"]
    want = [
        "Given I have a book due tomorrow",
        'When I click "Renew"',
        "Then the due date moves forward 14 days",
        "And I see a confirmation message",
    ]
    assert got == want, f"expected {want!r}, got {got!r}"


def test_complete_story_has_nothing_missing():
    got = parse_user_story(FULL)["missing"]
    assert got == [], f"expected [], got {got!r}"


def test_works_without_commas_and_in_lower_case():
    got = parse_user_story("as an admin i want to export users so that i can audit them\ngiven I am logged in")
    want = ("admin", "export users", "i can audit them")
    assert (got["role"], got["goal"], got["benefit"]) == want, f"expected {want!r}, got {(got['role'], got['goal'], got['benefit'])!r}"


def test_flags_missing_benefit_and_criteria():
    got = parse_user_story("As a shopper, I want to save my cart")
    assert got["benefit"] is None, f"expected None, got {got['benefit']!r}"
    assert got["missing"] == ["benefit", "criteria"], f"expected ['benefit', 'criteria'], got {got['missing']!r}"


def test_vague_ticket_is_missing_every_part():
    got = parse_user_story("Make the button blue")["missing"]
    want = ["role", "goal", "benefit", "criteria"]
    assert got == want, f"expected {want!r}, got {got!r}"
