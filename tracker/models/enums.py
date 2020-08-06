import enum

from sqlalchemy import asc, desc


class Sort(enum.Enum):
    ascending = "ascending"
    descending = "descending"

    @property
    def func(self):
        return asc if self == Sort.ascending else desc
