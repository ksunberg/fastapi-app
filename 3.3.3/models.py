from pydantic import BaseModel, validator, Field
from typing import Optional

MINIMUM_APP_VERSION = "0.0.2"


class CommonHeaders(BaseModel):
    user_agent: Optional[str] = Field(None, alias="User-Agent")
    accept_language: Optional[str] = Field(None, alias="Accept-Language")
    x_current_version: str = Field(
        ...,
        alias="X-Current-Version",
        pattern=r"^\d+\.\d+\.\d+$"
    )

    @validator('x_current_version')
    def check_version(cls, v):
        def to_tuple(version):
            return tuple(map(int, version.split('.')))
        if to_tuple(v) < to_tuple(MINIMUM_APP_VERSION):
            raise ValueError("Требуется обновить приложение")

        return v