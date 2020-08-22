import logging

from django.http import JsonResponse, Http404
from django.core.exceptions import ObjectDoesNotExist
from rest_framework import status as http_statuses
from rest_framework.exceptions import (
    NotAuthenticated,
    AuthenticationFailed,
    ValidationError,
)

from django_tea import errors as tea_errors

from traktor import errors


logger = logging.getLogger(__name__)


def format_rest_framework_validation_errors(errors):
    """Format error messages for response.

    Args:
        errors (dict): Dictionary of rest framework validation errors.

    Returns:
        dict: {field: error message}
    """
    if isinstance(errors, list):
        return ". ".join(str(e) for e in errors)
    elif isinstance(errors, dict):
        error = ""
        for key, value in errors.items():
            if key != "non_field_errors":
                error += f"{key}: "
            if isinstance(value, list):
                error += ". ".join(str(v) for v in value)
            else:
                error += str(value)
            error += "\n"
        return error.rstrip("\n")
    else:
        return str(errors)


def traktor_exception_handler(exc, context):
    if isinstance(exc, (NotAuthenticated, AuthenticationFailed)):
        data = {"error": str(exc)}
        status = http_statuses.HTTP_401_UNAUTHORIZED
    elif isinstance(
        exc,
        (
            ObjectDoesNotExist,
            Http404,
            tea_errors.ObjectNotFound,
            errors.TimerIsNotRunning,
        ),
    ):
        data = {"error": str(exc)}
        status = http_statuses.HTTP_404_NOT_FOUND
    elif isinstance(exc, ValidationError):
        data = {"error": format_rest_framework_validation_errors(exc.detail)}
        status = http_statuses.HTTP_400_BAD_REQUEST
    else:
        logger.error("API Error: %s", str(exc))
        data = {"error": str(exc)}
        status = http_statuses.HTTP_500_INTERNAL_SERVER_ERROR
    return JsonResponse(data, status=status)
