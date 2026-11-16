def match(pattern: str, path: str) -> dict | None:
    """The captured {placeholders} if path fits pattern, otherwise None."""
    pattern_parts = pattern.strip("/").split("/")
    path_parts = path.strip("/").split("/")
    if len(pattern_parts) != len(path_parts):
        return None
    params = {}
    for want, got in zip(pattern_parts, path_parts):
        if want.startswith("{") and want.endswith("}"):
            params[want[1:-1]] = got
        elif want != got:
            return None
    return params


class Router:
    def __init__(self):
        self.routes = []  # a list of (METHOD, pattern, handler)

    def add(self, method: str, pattern: str, handler) -> None:
        """Register handler for this method and path pattern."""
        self.routes.append((method.upper(), pattern, handler))

    def dispatch(self, method: str, path: str) -> tuple[int, object]:
        """Call the matching handler, or return a 404 / 405 response."""
        path_exists = False
        for route_method, pattern, handler in self.routes:
            params = match(pattern, path)
            if params is None:
                continue
            if route_method == method.upper():
                return handler(**params)
            path_exists = True
        if path_exists:
            return (405, {"error": "Method Not Allowed"})
        return (404, {"error": "Not Found"})


if __name__ == "__main__":
    router = Router()
    router.add("GET", "/tasks/{id}", lambda id: (200, {"id": id}))
    print(router.dispatch("GET", "/tasks/7"))
