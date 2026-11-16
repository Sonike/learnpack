import re
import unicodedata

from solution import check_slugify


def ascii_lower(title):
    return unicodedata.normalize("NFKD", title).encode("ascii", "ignore").decode("ascii").lower()


def correct(title):
    return re.sub(r"[^a-z0-9]+", "-", ascii_lower(title)).strip("-")


def caught(mutant):
    try:
        check_slugify(mutant)
    except Exception:
        return True
    return False


def test_correct_version_passes():
    try:
        check_slugify(correct)
    except AssertionError as e:
        raise AssertionError(f"your checker rejected a correct slugify: {e}") from None


def test_catches_capitals_and_missing_accent_handling():
    keeps_capitals = lambda t: re.sub(r"[^a-zA-Z0-9]+", "-", unicodedata.normalize("NFKD", t).encode("ascii", "ignore").decode()).strip("-")
    ignores_accents = lambda t: re.sub(r"[^a-z0-9]+", "-", t.lower()).strip("-")
    assert caught(keeps_capitals), "missed a slugify that keeps capital letters"
    assert caught(ignores_accents), "missed a slugify that drops accented letters instead of converting them (try 'Café')"


def test_catches_repeated_separators():
    one_dash_per_char = lambda t: re.sub(r"[^a-z0-9]", "-", ascii_lower(t)).strip("-")
    assert caught(one_dash_per_char), "missed a slugify that turns 'a -- b' into 'a----b'"


def test_catches_missing_or_half_stripping():
    no_strip = lambda t: re.sub(r"[^a-z0-9]+", "-", ascii_lower(t))
    right_strip_only = lambda t: re.sub(r"[^a-z0-9]+", "-", ascii_lower(t)).rstrip("-")
    assert caught(no_strip), "missed a slugify that leaves dashes at the ends (try a title with spaces around it)"
    assert caught(right_strip_only), "missed a slugify that only strips the trailing dash (try a leading space)"


def test_catches_space_only_replacement():
    spaces_only = lambda t: ascii_lower(t).strip().replace(" ", "-")
    assert caught(spaces_only), "missed a slugify that only replaces spaces and keeps punctuation like '&' or '!'"


def test_catches_dropped_digits_and_kept_underscores():
    drops_digits = lambda t: re.sub(r"[^a-z]+", "-", ascii_lower(t)).strip("-")
    keeps_underscores = lambda t: re.sub(r"[^a-z0-9_]+", "-", ascii_lower(t)).strip("-")
    assert caught(drops_digits), "missed a slugify that drops digits"
    assert caught(keeps_underscores), "missed a slugify that keeps underscores"
