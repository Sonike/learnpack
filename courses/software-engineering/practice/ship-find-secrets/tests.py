from solution import find_secrets


def test_flags_the_example_file():
    text = (
        "import os\n"
        'AWS_KEY = "AKIAABCDEFGHIJKLMNOP"\n'
        'password = os.environ["DB_PASSWORD"]\n'
        'api_key = "abc123"\n'
        "SECRET_KEY=\n"
        "STRIPE_SECRET=whsec_123\n"
    )
    got = find_secrets(text)
    want = [2, 4, 6]
    assert got == want, f"expected {want!r}, got {got!r}"


def test_flags_sk_keys_but_not_short_lookalikes():
    text = "key = get('sk-abcdefghijklmnopqrstuvwx')\nname = 'sk-short'\n"
    got = find_secrets(text)
    want = [1]
    assert got == want, f"expected {want!r}, got {got!r}"


def test_flags_quoted_secrets_in_json_and_any_case():
    text = '{"api_key": \'abc\', "user": "ada"}\nDB_Token = "t0k"\nPassword: "x"\n'
    got = find_secrets(text)
    want = [1, 2, 3]
    assert got == want, f"expected {want!r}, got {got!r}"


def test_ignores_env_lookups_empty_values_and_plain_code():
    text = (
        'password = os.environ["DB_PASSWORD"]\n'
        'token = ""\n'
        "API_KEY=\n"
        "def check_password(pw):\n"
        "    return len(pw) > 8\n"
    )
    got = find_secrets(text)
    want = []
    assert got == want, f"expected {want!r}, got {got!r}"


def test_empty_file_has_no_secrets():
    got = find_secrets("")
    want = []
    assert got == want, f"expected {want!r}, got {got!r}"
