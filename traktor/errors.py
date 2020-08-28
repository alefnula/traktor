from tea_django import errors


class TraktorError(errors.DjangoTeaError):
    pass


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
    def __init__(self, user: str, project_id: str):
        self.user = user
        self.project_id = project_id

        super().__init__(
            message=f"No default task found for user: {user}, "
            f"project: {project_id}."
        )
