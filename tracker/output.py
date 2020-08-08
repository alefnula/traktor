import json
from typing import List, Union, Type

import typer
import tabulate

from tracker.config import config
from tracker.models.model import Model


def output(model: Type[Model], objs: Union[List[Model], Model]):
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

        out = [[getattr(o, key) for key in model.HEADERS] for o in objs]

        print(
            tabulate.tabulate(
                out, headers=model.HEADERS, tablefmt="fancy_grid"
            )
        )
