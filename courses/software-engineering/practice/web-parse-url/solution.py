DEFAULT_PORTS = {"http": 80, "https": 443}


def parse_url(url: str) -> dict:
    """Split an absolute URL into scheme, host, port, path and query (as a dict)."""
    url, _, _fragment = url.partition("#")
    scheme, _, rest = url.partition("://")
    scheme = scheme.lower()
    rest, _, query_string = rest.partition("?")
    authority, slash, path = rest.partition("/")
    path = slash + path if slash else "/"
    host, colon, port = authority.partition(":")
    port = int(port) if colon else DEFAULT_PORTS[scheme]

    query = {}
    for pair in query_string.split("&"):
        if pair:
            key, _, value = pair.partition("=")
            query[key] = value

    return {"scheme": scheme, "host": host.lower(), "port": port, "path": path, "query": query}


if __name__ == "__main__":
    print(parse_url("HTTPS://Shop.Example.com/products/42?colour=red&size=m#reviews"))
    print(parse_url("http://localhost:8000"))
