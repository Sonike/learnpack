import copy

from solution import redact


def test_masks_top_level_sensitive_keys():
    got = redact({"user": "ada", "password": "hunter2", "token": "t"})
    want = {"user": "ada", "password": "***", "token": "***"}
    assert got == want, f"expected {want!r}, got {got!r}"


def test_matches_keys_ignoring_case_dashes_and_prefixes():
    got = redact({"X-API-Key": "k", "access_token": "a", "Client_Secret": "s", "Authorization": "Bearer x", "id": 7})
    want = {"X-API-Key": "***", "access_token": "***", "Client_Secret": "***", "Authorization": "***", "id": 7}
    assert got == want, f"expected {want!r}, got {got!r}"


def test_redacts_nested_dicts_and_dicts_inside_lists():
    data = {"headers": {"Authorization": "Bearer abc", "Accept": "json"}, "items": [{"sku": 1, "api_key": "k"}, 5]}
    got = redact(data)
    want = {"headers": {"Authorization": "***", "Accept": "json"}, "items": [{"sku": 1, "api_key": "***"}, 5]}
    assert got == want, f"expected {want!r}, got {got!r}"


def test_masks_a_sensitive_value_even_when_it_is_a_dict():
    got = redact({"secrets": {"a": 1}, "count": None})
    want = {"secrets": "***", "count": None}
    assert got == want, f"expected {want!r}, got {got!r}"


def test_does_not_change_the_original():
    data = {"password": "hunter2", "inner": {"token": "t"}, "list": [{"secret": "s"}]}
    before = copy.deepcopy(data)
    redact(data)
    assert data == before, f"expected {before!r}, got {data!r}"


def test_empty_dict_stays_empty():
    got = redact({})
    want = {}
    assert got == want, f"expected {want!r}, got {got!r}"
