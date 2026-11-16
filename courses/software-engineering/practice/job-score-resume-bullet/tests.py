from solution import score_resume_bullet


def check(text, want):
    got = score_resume_bullet(text)
    assert got == want, f"expected {want!r} for {text!r}, got {got!r}"


def test_strong_bullet_has_no_problems():
    check("- Built a FastAPI service with 14 endpoints and 92% test coverage", [])
    check("• Reduced page load time by 40% by caching database queries", [])


def test_responsible_for_bullet_gets_three_problems():
    check("Responsible for the backend of a group project", ["no action verb", "no number", "responsible for"])


def test_weak_verb_and_no_number():
    check("Worked on tests", ["no action verb", "no number"])


def test_action_verb_is_case_insensitive():
    check("SHIPPED 3 releases to 200 users", [])


def test_flags_bullet_over_200_characters():
    long_bullet = "Built " + "a very detailed feature " * 9 + "used by 50 people"
    assert len(long_bullet) > 200
    check(long_bullet, ["too long"])


def test_empty_bullet_has_no_verb_and_no_number():
    check("   ", ["no action verb", "no number"])
