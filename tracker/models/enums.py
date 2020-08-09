import enum
import string
from typing import Dict

import sqlalchemy as sa


class Sort(enum.Enum):
    ascending = "ascending"
    descending = "descending"

    @property
    def func(self):
        return sa.asc if self == Sort.ascending else sa.desc


class RGB:
    """RGB color model."""

    def __init__(self, r: int = 0, g: int = 0, b: int = 0):
        for i in [r, g, b]:
            if not isinstance(i, int) or (i < 0 or i > 255):
                raise ValueError(f"Invalid value for RGB: r={r}, g={g}, b={b}")
        self.r = r
        self.g = g
        self.b = b

    def __eq__(self, other):
        return self.r == other.r and self.g == other.g and self.b == other.b

    def __str__(self):
        return f"RGB(r={self.r}, g={self.g}, b={self.b})"

    __repr__ = __str__

    @property
    def hex(self):
        return f"#{self.r:02x}{self.g:02x}{self.b:02x}"

    @property
    def rich(self):
        return f"rgb({self.r},{self.g},{self.b})"

    @classmethod
    def parse(cls, color: str) -> "RGB":
        if (
            not color.startswith("#")
            and len(color) == 7
            and all([color[i] in string.hexdigits for i in range(1, 8)])
        ):
            raise ValueError(f"Invalid color string: {color}")

        return cls(
            r=int(color[1:3], 16),
            g=int(color[3:5], 16),
            b=int(color[5:7], 16),
        )

    def to_dict(self) -> Dict[str, int]:
        return {"r": self.r, "g": self.g, "b": self.b}

    @classmethod
    def from_dict(cls, d: Dict[str, int]) -> "RGB":
        return cls(r=d["r"], g=d["g"], b=d["b"])
