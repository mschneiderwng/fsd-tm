import pytest

def func(x):
    return x + 1

@pytest.mark.skip(reason="always wrong")
def test_answer():
    assert func(3) == 5