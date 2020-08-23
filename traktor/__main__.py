import os
import sys
from pathlib import Path


def main():
    # Setup environment

    # Setup python path
    module_dir = str(Path(__file__).parents[1].absolute())
    if module_dir not in sys.path:
        sys.path.insert(0, module_dir)
    python_path = os.environ.get("PYTHONPATH", "").strip()
    if python_path == "":
        os.environ.setdefault("PYTHONPATH", module_dir)
    else:
        if module_dir not in python_path.split(":"):
            os.environ.setdefault(
                "PYTHONPATH", f"{module_dir}:{python_path.lstrip(':')}"
            )

    # Setup django setting module
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "traktor.settings")

    # Setup django
    import django

    django.setup()

    args = sys.argv[:]
    # Check if it's a django manage command and run it
    if len(args) >= 2 and args[0].endswith("traktor") and args[1] == "manage":
        from django.core.management import execute_from_command_line

        execute_from_command_line(args[:1] + args[2:])
    # If not run the application
    else:
        from traktor.commands import app

        app()


if __name__ == "__main__":
    main()
