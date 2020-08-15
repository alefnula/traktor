import enum
import string
from typing import Tuple

import sqlalchemy as sa


class Sort(enum.Enum):
    ascending = "ascending"
    descending = "descending"

    @property
    def func(self):
        return sa.asc if self == Sort.ascending else sa.desc


class RGB:
    """RGB color model."""

    @staticmethod
    def __check_color_string(color: str) -> str:
        color = color.strip()
        if (
            len(color) == 7
            and color[0] == "#"
            and all([color[i] in string.hexdigits for i in range(1, 7)])
        ):
            return color[1:]
        elif len(color) == 6 and all(
            [color[i] in string.hexdigits for i in range(6)]
        ):
            return color
        else:
            raise ValueError(f"Invalid color string: {color}")

    def __init__(self, color="#000000"):
        color = self.__check_color_string(color=color)

        self.r = int(color[:2], 16)
        self.g = int(color[2:4], 16)
        self.b = int(color[4:], 16)

    def __eq__(self, other):
        return self.r == other.r and self.g == other.g and self.b == other.b

    def __str__(self):
        return f"RGB(r={self.r}, g={self.g}, b={self.b})"

    __repr__ = __str__

    @property
    def tuple(self) -> Tuple[int, int, int]:
        return self.r, self.g, self.b

    @property
    def hex(self):
        return f"#{self.r:02x}{self.g:02x}{self.b:02x}"

    @property
    def rich(self):
        return f"rgb({self.r},{self.g},{self.b})"

    def to_dict(self) -> str:
        return self.hex
