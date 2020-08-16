import pytest

from traktor.models.enums import RGB


def test_rgb_parse():
    # With hash
    assert RGB("#010203").tuple == (1, 2, 3)
    assert RGB("#2164FF").tuple == (33, 100, 255)

    # Without hash
    assert RGB("010203").tuple == (1, 2, 3)
    assert RGB("2164FF").tuple == (33, 100, 255)

    with pytest.raises(ValueError):
        RGB("0000000")

    with pytest.raises(ValueError):
        RGB("#0000000")

    with pytest.raises(ValueError):
        RGB("#0000G0")
