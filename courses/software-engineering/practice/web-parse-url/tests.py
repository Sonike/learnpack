from urllib.parse import parse_qsl, urlsplit

from solution import parse_url


def expected(url):
    """What urllib.parse says, in the same shape."""
    parts = urlsplit(url)
    default = {"http": 80, "https": 443}[parts.scheme]
    return {
        "scheme": parts.scheme,
        "host": parts.hostname,
        "port": parts.port or default,
        "path": parts.path or "/",
        "query": dict(parse_qsl(parts.query, keep_blank_values=True)),
    }


def check(url):
    got, want = parse_url(url), expected(url)
    assert got == want, f"for {url!r}: expected {want!r}, got {got!r}"


def test_full_url_with_port_query_and_fragment():
    check("https://shop.example.com:8443/products/42?colour=red&size=m#reviews")


def test_default_ports_for_http_and_https():
    check("http://example.com/about")
    check("https://example.com/about")


def test_missing_path_becomes_slash():
    check("http://localhost:8000")
    check("https://example.com?q=1")


def test_scheme_and_host_are_lower_cased():
    check("HTTPS://Shop.Example.COM/Products")


def test_query_edge_cases():
    check("https://api.example.com/search?q=&page=2&debug")
    check("https://api.example.com/search")


def test_fragment_is_ignored():
    got = parse_url("https://example.com/docs#install?x=1")
    want = {"scheme": "https", "host": "example.com", "port": 443, "path": "/docs", "query": {}}
    assert got == want, f"expected {want!r}, got {got!r}"
