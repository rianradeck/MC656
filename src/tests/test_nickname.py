import pytest

from utils.utils import nickname_is_valid


@pytest.fixture()
def good_nickname_letters():
    return "igor"


@pytest.fixture()
def good_nickname_numbers():
    return "0123456789"


@pytest.fixture()
def bad_nickname_long():
    return "a" * 13


@pytest.fixture()
def bad_nickname_short():
    return "a" * 3


@pytest.fixture()
def bad_nickname_upper():
    return "A" * 8


@pytest.fixture()
def bad_nickname_special():
    return "@@@@"


def test_nickname_input(
    good_nickname_letters,
    good_nickname_numbers,
    bad_nickname_long,
    bad_nickname_short,
    bad_nickname_upper,
    bad_nickname_special,
):
    assert nickname_is_valid(good_nickname_letters)
    assert nickname_is_valid(good_nickname_numbers)
    assert not nickname_is_valid(bad_nickname_long)
    assert not nickname_is_valid(bad_nickname_short)
    assert not nickname_is_valid(bad_nickname_upper)
    assert not nickname_is_valid(bad_nickname_special)
