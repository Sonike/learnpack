class Router:
    def __init__(self):
        self.routes = []  # a list of (METHOD, pattern, handler)

    def add(self, method: str, pattern: str, handler) -> None:
        """Register handler for this method and path pattern."""
        # TODO: store the route
        pass

    def dispatch(self, method: str, path: str) -> tuple[int, object]:
        """Call the matching handler, or return a 404 / 405 response."""
        # TODO: for each route, try to match the pattern against the path.
        #       Pattern matches + method matches -> return handler(**params)
        #       Pattern matches, wrong method -> remember it, answer 405 at the end
        return (404, {"error": "Not Found"})


if __name__ == "__main__":
    router = Router()
    router.add("GET", "/tasks", lambda: (200, ["all tasks"]))
    router.add("GET", "/tasks/{id}", lambda id: (200, {"id": id}))
    print(router.dispatch("GET", "/tasks/7"))
    print(router.dispatch("DELETE", "/tasks/7"))
    print(router.dispatch("GET", "/banana"))
