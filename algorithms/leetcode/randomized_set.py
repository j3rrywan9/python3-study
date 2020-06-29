# LC 380
from random import choice


class RandomizedSet:
    def __init__(self):
        self.dict = {}
        self.list = []

    def insert(self, val):
        if val in self.dict:
            return False

        self.dict[val] = len(self.list)
        self.list.append(val)

        return True

    def remove(self, val):
        if val not in self.dict:
            return False

        # move the last element to the index of the element to delete
        last_element, index = self.list[-1], self.dict[val]
        self.list[index], self.dict[last_element] = last_element, index
        # delete the last element
        self.list.pop()
        del self.dict[val]
        return True

    def get_random(self):
        return choice(self.list)
