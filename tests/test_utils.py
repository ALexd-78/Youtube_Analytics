import pytest

from utils import Channel


def test_str():
    __channel_id = Channel('UCMCgOm8GZkHp8zJ6l7_hIuA')
    assert __channel_id.__str__() == "Youtube-канал: вДудь"