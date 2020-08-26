from ..leap_frog_jumper import Solution


def test_example1():
    assert Solution().get_char_at_index('leap2frog3jumper2', 42) == "l"


def test_example2():
    assert Solution().get_char_at_index('leap2frog3jumper2', 4242) == ""
