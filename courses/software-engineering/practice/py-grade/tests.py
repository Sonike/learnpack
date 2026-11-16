from solution import grade


def test_middle_of_each_band():
    for score, want in [(95, "A"), (85, "B"), (75, "C"), (65, "D"), (30, "F")]:
        got = grade(score)
        assert got == want, f"grade({score}): expected {want!r}, got {got!r}"


def test_band_boundaries():
    cases = [(100, "A"), (90, "A"), (89, "B"), (80, "B"), (79, "C"), (70, "C"),
             (69, "D"), (60, "D"), (59, "F"), (0, "F")]
    for score, want in cases:
        got = grade(score)
        assert got == want, f"grade({score}): expected {want!r}, got {got!r}"


def test_rejects_scores_above_100():
    try:
        got = grade(101)
    except ValueError:
        return
    assert False, f"grade(101) should raise ValueError, but returned {got!r}"


def test_rejects_negative_scores():
    try:
        got = grade(-1)
    except ValueError:
        return
    assert False, f"grade(-1) should raise ValueError, but returned {got!r}"
