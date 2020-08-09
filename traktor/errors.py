from typing import Type


class TraktorError(Exception):
    def __init__(self, message: str):
        self.message = message

    @property
    def class_name(self):
        return self.__class__.__name__

    def __str__(self):
        return f"{self.class_name}({self.message})"

    __repr__ = __str__


class InvalidConfiguration(TraktorError):
    def __init__(
        self, key: str = None, value: str = None, valid_values: str = None
    ):
        if key is not None and value is not None:
            message = f"Invalid configuration key=`{key}` and value=`{value}`."
        elif key is not None:
            message = f"Invalid configuration key=`{key}`."
        elif value is not None:
            message = f"Invalid configuration value=`{value}`."
        else:
            message = "Invalid configuration."

        if valid_values is not None:
            message += f" Valid values: `{valid_values}`"

        super().__init__(message=message)


class ObjectNotFound(TraktorError):
    def __init__(self, model: Type, query: dict):
        """DeviceNotFound error.

        Args:
            model: Model class.
            query: Query dictionary.
        """
        self.model = model
        self.query = query

        if len(query) == 0:
            query_string = ""
        else:
            query_string = (
                "("
                + ", ".join(f"{key}={value}" for key, value in query.items())
                + ")"
            )
        super().__init__(
            message=f"{model.class_name()}{query_string} not found."
        )


class TimerAlreadyRunning(TraktorError):
    def __init__(self, timers: list):
        self.timers = timers

        super().__init__(message="Timer is already running.",)


class NoDefaultTask(TraktorError):
    def __init__(self, project: str):
        self.project = project

        super().__init__(
            message=f"No default task found for project: {project}."
        )
