import pytest
from utils import Channel


@pytest.fixture()
def ch1():
    return Channel('UCMCgOm8GZkHp8zJ6l7_hIuA')


@pytest.fixture()
def ch2():
    return Channel('UC1eFXmJNkjITxPFWTy6RsWg')

def test_str():
    ch1 = Channel('UCMCgOm8GZkHp8zJ6l7_hIuA')
    assert ch1.__str__() == "Youtube-канал: вДудь"


def test_lt(ch1, ch2):
    assert ch1.__lt__(ch2) is False

def test_add(ch1, ch2):
    ch1 = Channel('UCMCgOm8GZkHp8zJ6l7_hIuA')
    ch2 = Channel('UC1eFXmJNkjITxPFWTy6RsWg')
    assert ch1.__add__(ch2) == 14000000
