from solution import word_ladder_length

WORDS = ["hot", "dot", "dog", "lot", "log", "cog"]


def check(begin, end, words, want):
    got = word_ladder_length(begin, end, words)
    assert got == want, f"expected {want!r} for {begin!r} -> {end!r}, got {got!r}"


def test_classic_example():
    check("hit", "cog", WORDS, 5)


def test_end_word_missing_returns_zero():
    check("hit", "cog", WORDS[:-1], 0)


def test_one_step():
    check("hot", "dot", ["dot"], 2)


def test_unreachable_returns_zero():
    check("abc", "xyz", ["abd", "xyz"], 0)


def test_finds_shortest_not_first_path():
    words = ["bat", "bit", "bot", "cot", "cog", "bog", "cat"]
    # bat -> bot -> bog -> cog is 4; bat -> cat -> cot -> cog is also 4
    check("bat", "cog", words, 4)
