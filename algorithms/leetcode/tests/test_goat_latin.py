#!/usr/bin/env python3
from ..goat_latin import Solution


def test_example1():
    assert Solution().to_goat_latin("I speak Goat Latin") == "Imaa peaksmaaa oatGmaaaa atinLmaaaaa"


def test_example2():
    assert Solution().to_goat_latin("The quick brown fox jumped over the lazy dog") == \
           "heTmaa uickqmaaa rownbmaaaa oxfmaaaaa umpedjmaaaaaa overmaaaaaaa hetmaaaaaaaa azylmaaaaaaaaa ogdmaaaaaaaaaa"
