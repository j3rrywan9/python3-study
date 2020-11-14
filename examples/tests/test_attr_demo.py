import attr
import pytest

from ..attr_demo import SomeClass


@pytest.fixture(scope="module")
def some_object():
    return SomeClass(1, [1, 2, 3])


def test_equality(some_object):
    assert some_object == SomeClass(1, [1, 2, 3])
    assert some_object != SomeClass(2, [3, 2, 1])


def test_asdict(some_object):
    assert attr.asdict(some_object) == {'a_number': 1, 'list_of_numbers': [1, 2, 3]}
