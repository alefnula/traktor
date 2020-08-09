import json
from typing import List, Union, Type

import typer
from rich.table import Table
from rich.console import Console


from traktor.config import config
from traktor.models import VanillaModel, Model


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
        if isinstance(objs, list):
            out = [o.to_dict() for o in objs]
        else:
            out = objs.to_dict()
        print(json.dumps(out, indent=4))

    elif config.format == config.Format.text:
        if not isinstance(objs, list):
            objs = [objs]

        if len(objs) == 0:
            typer.secho(
                f"No {model.class_name()}s found.", fg=typer.colors.CYAN
            )
            return

        console = Console()
        table = Table(show_header=True, header_style="bold magenta")
        for column in model.HEADERS:
            table.add_column(header=column.title, justify=column.align)

        for o in objs:
            table.add_row(
                *[get_path(o, column.path) for column in model.HEADERS]
            )

        console.print(table)
