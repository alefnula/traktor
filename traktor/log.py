import os


def create_logging_configuration(log_dir, hosted=False):
    """Create logging configuration.

    Args:
        log_dir (str): Path to the log directory
        hosted (bool): Is this hosted or development environment.
    """
    # Create if it doesn't exist
    os.makedirs(log_dir, exist_ok=True)

    max_bytes = 1024 * 1024 * 1024  # max log size: 1 GB

    return {
        "version": 1,
        "disable_existing_loggers": True,
        "formatters": {
            "verbose": {
                "format": (
                    "{asctime} {levelname} {name} {message} "
                    "fileName={filename} func={funcName} lineNum={lineno} "
                    "threadName={threadName} process={process}"
                ),
                "style": "{",
            },
            "simple": {
                "format": "{asctime} {levelname} {message} {module}",
                "style": "{",
            },
        },
        "handlers": {
            "traktor": {
                "level": "DEBUG",
                "class": "logging.handlers.RotatingFileHandler",
                "filename": os.path.join(log_dir, "traktor.log"),
                "maxBytes": max_bytes,
                "backupCount": 5,
                "formatter": "verbose",
            },
            "traktor-error": {
                "level": "ERROR",
                "class": "logging.handlers.RotatingFileHandler",
                "filename": os.path.join(log_dir, "traktor-error.log"),
                "maxBytes": max_bytes,
                "backupCount": 5,
                "formatter": "verbose",
            },
            "traktor-console": {
                "level": "INFO",
                "class": "logging.StreamHandler",
                "formatter": "simple",
            },
        },
        "loggers": {
            "": {
                "level": "INFO",
                "handlers": ["traktor", "traktor-error"]
                + ([] if hosted else ["traktor-console"]),
            },
            "traktor": {
                "level": "INFO",
                "handlers": ["traktor", "traktor-error"]
                + ([] if hosted else ["traktor-console"]),
                "propagate": False,
            },
            # 3rd Party Software Logs
            "django": {
                "level": "INFO",
                "handlers": ["traktor", "traktor-error"]
                + ([] if hosted else ["traktor-console"]),
                "propagate": True,
            },
            "django.request": {
                "level": "ERROR",
                "handlers": ["traktor", "traktor-error"]
                + ([] if hosted else ["traktor-console"]),
                "propagate": False,
            },
            "django.server": {
                "level": "INFO",
                "handlers": ["traktor", "traktor-error"]
                + ([] if hosted else ["traktor-console"]),
                "propagate": False,
            },
            "django.db.backends": {
                "level": "ERROR",
                "handlers": ["traktor", "traktor-error"]
                + ([] if hosted else ["traktor-console"]),
                "propagate": False,
            },
        },
    }
