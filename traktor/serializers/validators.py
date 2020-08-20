from django_tea.consts import COLOR_RE
from rest_framework.exceptions import ValidationError


def color_validator(value):
    if COLOR_RE.match(value) is None:
        raise ValidationError(f"Invalid color string: {value}")
    return value
