import json
from typing import List, Union, Type

import typer
from rich import print
from rich.table import Table
from rich.console import Console


from traktor.config import config
from traktor.models import VanillaModel, Model

# Json


class TraktorEncoder(json.JSONEncoder):
    """Tea JSON Encoder.

    It knows how to serialize:

        1. All objects that have a custom `to_dict` method
        2. Decimal numbers
        3. DateTime and Date objects
    """

    to_float = frozenset(("decimal.Decimal",))
    to_datetime = frozenset(("datetime.datetime", "datetime.date"))
    to_list = frozenset(
        (
            "__builtin__.set",
            "builtins.set",
            "builtins.dict_keys",
            "builtins.dict_values",
        )
    )

    def __init__(self, *args, **kwargs):
        self.datetime_format = kwargs.pop(
            "datetime_format", "%Y-%m-%dT%H:%M:%S"
        )
        super(TraktorEncoder, self).__init__(*args, **kwargs)

    def default(self, o):
        try:
            return super(TraktorEncoder, self).default(o)
        except TypeError:
            # First see if there is a __json__ method
            if hasattr(o, "to_dict"):
                return o.to_dict()
            # Then try out special classes
            cls = o.__class__
            path = "%s.%s" % (cls.__module__, cls.__name__)
            if path in self.to_float:
                return float(o)
            elif path in self.to_datetime:
                return o.strftime(self.datetime_format)
            elif path in self.to_list:
                return list(o)
            raise TypeError("%s is not JSON serializable" % o)


def json_dumps(obj, encoding=None, indent=4) -> Union[bytes, str]:
    """Wrap `json.dumps` using the `TraktorEncoder`."""
    s = json.dumps(
        obj,
        cls=TraktorEncoder,
        ensure_ascii=False,
        allow_nan=False,
        indent=indent,
        separators=(",", ":"),
    )
    return s if encoding is None else s.encode(encoding=encoding)


# Table
def get_path(obj, path) -> str:
    path = path.split(".")
    for item in path:
        obj = getattr(obj, item)
    if isinstance(obj, bool):
        return ":white_check_mark:" if obj else ":cross_mark:"
    return str(obj)


ModelClass = Union[VanillaModel, Model]


def output(model: Type[ModelClass], objs: Union[List[ModelClass], ModelClass]):
    if config.format == config.Format.json:
        print(json_dumps(objs))

    elif config.format == config.Format.text:
        if objs is None or (isinstance(objs, list) and len(objs) == 0):
            typer.secho(
                f"No {model.class_name()}s found.", fg=typer.colors.CYAN
            )
            return

        if not isinstance(objs, list):
            objs = [objs]

        console = Console()
        table = Table(show_header=True, header_style="bold magenta")
        for column in model.HEADERS:
            table.add_column(header=column.title, justify=column.align)

        for o in objs:
            table.add_row(
                *[get_path(o, column.path) for column in model.HEADERS]
            )

        console.print(table)
