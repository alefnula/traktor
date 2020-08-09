import pytest

from traktor.models.enums import RGB


def test_rgb_creation_type():
    # Positive
    assert RGB(r=22, g=44, b=55) == RGB(22, 44, 55)
    assert RGB(r=0xA) == RGB(10, 0, 0)
    assert RGB(r=0o10) == RGB(8, 0, 0)

    # Negative
    # float
    with pytest.raises(ValueError):
        RGB(r=1.0)

    # str
    with pytest.raises(ValueError):
        RGB(r="1")


def test_rgb_cration_out_of_range():
    # Positive
    for r in range(0, 255, 5):
        for g in range(0, 255, 5):
            for b in range(0, 255, 5):
                RGB(r=r, g=g, b=b)

    with pytest.raises(ValueError):
        RGB(r=-1)

    with pytest.raises(ValueError):
        RGB(r=256)


def test_rgb_str():
    assert RGB(r=1, g=2, b=3).hex == "#010203"
    assert RGB(r=33, g=100, b=255).hex == "#2164ff"


def test_rgb_parse():
    # With hash
    assert RGB.parse("#010203") == RGB(1, 2, 3)
    assert RGB.parse("#2164FF") == RGB(33, 100, 255)

    # Without hash
    assert RGB.parse("010203") == RGB(1, 2, 3)
    assert RGB.parse("2164FF") == RGB(33, 100, 255)
