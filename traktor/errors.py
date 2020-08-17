from typing import Type, Optional


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
    def __init__(self, key: str, value: str, error: Exception):
        super().__init__(
            message=f"Error setting '{key}' to '{value}'. Error: {error}"
        )


def query_to_string(query: Optional[dict]) -> str:
    if query is None or len(query) == 0:
        return ""
    else:
        return (
            "("
            + ", ".join(f"{key}={value}" for key, value in query.items())
            + ")"
        )


class ObjectAlreadyExists(TraktorError):
    def __init__(self, model: Type, query: Optional[dict] = None):
        self.model = model
        self.query = query

        super().__init__(
            message=(
                f"{model.class_name}{query_to_string(self.query)} "
                f"already exists."
            )
        )


class ObjectNotFound(TraktorError):
    def __init__(self, model: Type, query: Optional[dict] = None):
        """ObjectNotFound error.

        Args:
            model: Model class.
            query: Query dictionary.
        """
        self.model = model
        self.query = query

        super().__init__(
            message=(
                f"{model.class_name}{query_to_string(self.query)} not found."
            )
        )


class MultipleObjectsFound(TraktorError):
    def __init__(self, model: Type, query: Optional[dict] = None):
        """MultipleObjectsFound error.

        Args:
            model: Model class.
            query: Query dictionary.
        """
        self.model = model
        self.query = query

        super().__init__(
            message=(
                f"{model.class_name}{query_to_string(self.query)} "
                f"multiple objects found."
            )
        )


class TimerAlreadyRunning(TraktorError):
    def __init__(self, project_id: str, task_id: str):
        self.project_id = project_id
        self.task_id = task_id

        super().__init__(
            message=f"Timer is already running for {project_id}/{task_id}."
        )


class TimerIsNotRunning(TraktorError):
    def __init__(self):
        super().__init__(message="Timer is not running.")


class NoDefaultTask(TraktorError):
    def __init__(self, project_id: str):
        self.project_id = project_id

        super().__init__(
            message=f"No default task found for project: {project_id}."
        )
