from solution import first_bad_version


def counting(first_bad_name, versions):
    """An is_bad that records every call. Versions from first_bad_name onwards are bad."""
    cutoff = versions.index(first_bad_name) if first_bad_name else len(versions)
    calls = []

    def is_bad(version):
        calls.append(version)
        return versions.index(version) >= cutoff

    return is_bad, calls


def test_finds_the_first_bad_version_in_a_short_list():
    versions = ["v1", "v2", "v3", "v4", "v5", "v6"]
    is_bad, _ = counting("v4", versions)
    got = first_bad_version(versions, is_bad)
    assert got == 3, f"expected 3, got {got!r}"


def test_the_very_first_version_can_be_bad():
    versions = ["a", "b", "c"]
    is_bad, _ = counting("a", versions)
    got = first_bad_version(versions, is_bad)
    assert got == 0, f"expected 0, got {got!r}"


def test_returns_minus_one_when_nothing_is_bad():
    versions = ["a", "b", "c"]
    is_bad, _ = counting(None, versions)
    got = first_bad_version(versions, is_bad)
    assert got == -1, f"expected -1, got {got!r}"


def test_empty_history_returns_minus_one():
    got = first_bad_version([], lambda v: True)
    assert got == -1, f"expected -1, got {got!r}"


def test_uses_few_checks_on_a_long_history():
    versions = [f"c{n:04d}" for n in range(1000)]
    for first_bad in ["c0000", "c0613", "c0999"]:
        is_bad, calls = counting(first_bad, versions)
        got = first_bad_version(versions, is_bad)
        want = versions.index(first_bad)
        assert got == want, f"expected {want!r}, got {got!r}"
        assert len(calls) <= 11, f"called is_bad {len(calls)} times; binary search needs at most 11"
