DEFAULT_PORTS = {"http": 80, "https": 443}


def parse_url(url: str) -> dict:
    """Split an absolute URL into scheme, host, port, path and query (as a dict)."""
    # TODO 1: drop the fragment (everything from '#')
    # TODO 2: split the scheme off at '://'
    # TODO 3: split the query off at '?', and turn 'a=1&b=2' into {'a': '1', 'b': '2'}
    # TODO 4: split host[:port] from the path at the first '/'
    # TODO 5: split host and port at ':' (or use the default port)
    return {"scheme": "", "host": "", "port": 0, "path": "/", "query": {}}


if __name__ == "__main__":
    print(parse_url("HTTPS://Shop.Example.com/products/42?colour=red&size=m#reviews"))
    print(parse_url("http://localhost:8000"))
