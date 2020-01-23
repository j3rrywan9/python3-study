#!/usr/bin/env python3

from collections.abc import Container


class OddContainer:
    def __contains__(self, x):
        if not isinstance(x, int) or not x % 2:
            return False
        return True


def main():
    odd_container = OddContainer()

    assert isinstance(odd_container, Container)
    assert issubclass(OddContainer, Container)

    assert 1 in odd_container
    assert 2 not in odd_container
    assert 3 in odd_container
    assert "a string" not in odd_container


if __name__ == "__main__":
    main()
