import pytest
from string_utils import index_of_difference


def test_none_none():
    with pytest.raises(TypeError):
        index_of_difference(None, None)


def test_empty_strings():
    assert index_of_difference("", "") == -1


def test_empty_and_nonempty():
    assert index_of_difference("", "abc") == 0
    assert index_of_difference("abc", "") == 0


def test_equal_strings():
    assert index_of_difference("abc", "abc") == -1


def test_difference_middle():
    assert index_of_difference("i am a machine", "i am a robot") == 7


def test_prefix_case():
    assert index_of_difference("ab", "abxyz") == 2


def test_difference():
    assert index_of_difference("abcde", "abxyz") == 2


def test_full_difference():
    assert index_of_difference("abcde", "xyz") == 0
