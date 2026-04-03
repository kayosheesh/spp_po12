import pytest
from main import Razmah
from task2 import maxPrefix, sortBubble



def test_razmah_normal():
    assert Razmah([6, 4, 2, 6, -2, 5, 8]) == 10


def test_razmah_one_element():
    assert Razmah([5]) == 0


def test_razmah_negative_numbers():
    assert Razmah([-10, -5, -1]) == 9


def test_razmah_empty():
    with pytest.raises(ValueError):
        Razmah([])


def test_razmah_none():
    with pytest.raises(TypeError):
        Razmah(None)



def test_maxprefix_normal():
    assert maxPrefix(["flower", "flow", "flight"]) == "f.l"


def test_maxprefix_no_common():
    assert maxPrefix(["dog", "racecar", "car"]) == ""


def test_maxprefix_one_string():
    assert maxPrefix(["abc"]) == "a.b.c"


def test_maxprefix_empty_strings():
    assert maxPrefix(["", ""]) == ""


def test_maxprefix_none():
    with pytest.raises(TypeError):
        maxPrefix(None)


def test_sortbubble_normal():
    assert sortBubble([3, 1, 4, 2]) == [4, 3, 2, 1]


def test_sortbubble_already_sorted():
    assert sortBubble([5, 4, 3]) == [5, 4, 3]


def test_sortbubble_with_duplicates():
    assert sortBubble([2, 2, 1]) == [2, 2, 1]


def test_sortbubble_strings():
    assert sortBubble(["a", "c", "b"]) == ["c", "b", "a"]


def test_sortbubble_empty():
    assert sortBubble([]) == []


def test_sortbubble_none():
    with pytest.raises(TypeError):
        sortBubble(None)
