from ..heap.top_k_frequent_words import Solution


def test_example1():
    assert Solution().top_k_frequent(["i", "love", "leetcode", "i", "love", "coding"], 2) == ["i", "love"]


def test_example2():
    assert Solution().top_k_frequent(["the", "day", "is", "sunny", "the", "the", "the", "sunny", "is", "is"], 4) == \
           ["the", "is", "sunny", "day"]
