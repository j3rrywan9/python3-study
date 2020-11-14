import attr

from typing import List


@attr.s(auto_attribs=True)
class SomeClass:
    a_number: int = 42
    list_of_numbers: List[int] = attr.Factory(list)

    def hard_math(self, another_number):
        return self.a_number + sum(self.list_of_numbers) * another_number
