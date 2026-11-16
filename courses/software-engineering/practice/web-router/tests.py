from solution import Router

NOT_FOUND = (404, {"error": "Not Found"})
NOT_ALLOWED = (405, {"error": "Method Not Allowed"})


def make_router():
    router = Router()
    router.add("GET", "/tasks", lambda: (200, "list"))
    router.add("POST", "/tasks", lambda: (201, "create"))
    router.add("GET", "/tasks/{id}", lambda id: (200, {"get": id}))
    router.add("DELETE", "/tasks/{id}", lambda id: (204, {"delete": id}))
    router.add("GET", "/users/{uid}/tasks/{tid}", lambda uid, tid: (200, {"uid": uid, "tid": tid}))
    return router


def test_routes_fixed_paths_by_method():
    router = make_router()
    for method, path, want in [("GET", "/tasks", (200, "list")), ("POST", "/tasks", (201, "create"))]:
        got = router.dispatch(method, path)
        assert got == want, f"{method} {path}: expected {want!r}, got {got!r}"


def test_captures_path_parameters_as_strings():
    router = make_router()
    got = router.dispatch("GET", "/tasks/42")
    assert got == (200, {"get": "42"}), f"expected {(200, {'get': '42'})!r}, got {got!r}"
    got = router.dispatch("GET", "/users/3/tasks/9")
    want = (200, {"uid": "3", "tid": "9"})
    assert got == want, f"expected {want!r}, got {got!r}"


def test_unknown_path_is_404():
    router = make_router()
    for path in ["/banana", "/tasks/1/extra", "/users/3/tasks"]:
        got = router.dispatch("GET", path)
        assert got == NOT_FOUND, f"GET {path}: expected {NOT_FOUND!r}, got {got!r}"


def test_known_path_with_wrong_method_is_405():
    router = make_router()
    for method, path in [("DELETE", "/tasks"), ("PUT", "/tasks/7")]:
        got = router.dispatch(method, path)
        assert got == NOT_ALLOWED, f"{method} {path}: expected {NOT_ALLOWED!r}, got {got!r}"


def test_methods_are_case_insensitive_and_slashes_are_ignored():
    router = make_router()
    got = router.dispatch("delete", "/tasks/5/")
    assert got == (204, {"delete": "5"}), f"expected {(204, {'delete': '5'})!r}, got {got!r}"


def test_empty_router_answers_404():
    got = Router().dispatch("GET", "/")
    assert got == NOT_FOUND, f"expected {NOT_FOUND!r}, got {got!r}"
