from ..integer_to_english_words import Solution


def test_example1():
    assert Solution().numberToWords(123) == 'One Hundred Twenty Three'


def test_example2():
    assert Solution().numberToWords(12345) == 'Twelve Thousand Three Hundred Forty Five'


def test_example3():
    assert Solution().numberToWords(1234567) == 'One Million Two Hundred Thirty Four Thousand Five Hundred Sixty Seven'


def test_example4():
    assert Solution().numberToWords(1234567891) == \
           'One Billion Two Hundred Thirty Four Million Five Hundred Sixty Seven Thousand Eight Hundred Ninety One'
