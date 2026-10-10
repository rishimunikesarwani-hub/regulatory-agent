"""Shared strict value types for API and telemetry contracts."""
from typing import Annotated
from pydantic import BaseModel, ConfigDict, Field


Identifier = Annotated[str, Field(min_length=1, max_length=128, pattern=r"^[A-Za-z0-9][A-Za-z0-9_.:-]*$")]


class Contract(BaseModel):
    model_config = ConfigDict(extra="forbid", strict=True, frozen=True)
