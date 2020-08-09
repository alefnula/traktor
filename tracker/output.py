import json
from typing import List, Union, Type

import typer
from rich.table import Table
from rich.console import Console


from tracker.config import config
from tracker.models import Model, Report


def get_path(obj, path):
    path = path.split(".")
    for item in path:
        obj = getattr(obj, item)
    return obj


def output(model: Type[Union[Model, Report]], objs: Union[List[Model], Model]):
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
        for name, _ in model.HEADERS:
            table.add_column(name)

        for o in objs:
            table.add_row(*[get_path(o, path) for _, path in model.HEADERS])

        console.print(table)
