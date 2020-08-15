from typing import Optional

from pydantic import BaseModel, validator

from traktor.models import RGB


class ProjectCreateRequest(BaseModel):
    name: str
    color: Optional[str] = None

    @validator("color")
    def validate_color(cls, value):
        RGB.parse(value)
        return value


class ProjectUpdateRequest(BaseModel):
    name: Optional[str] = None
    color: Optional[str] = None

    @validator("color")
    def validate_color(cls, value):
        RGB.parse(value)
        return value
