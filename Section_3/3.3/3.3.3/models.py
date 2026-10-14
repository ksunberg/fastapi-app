from pydantic import BaseModel, Field, field_validator

MINIMUM_APP_VERSION = "0.0.2"


class CommonHeaders(BaseModel):
    user_agent: str | None = Field(None, alias="User-Agent")
    accept_language: str | None = Field(None, alias="Accept-Language")
    x_current_version: str = Field(
        ...,
        alias="X-Current-Version",
        pattern=r"^\d+\.\d+\.\d+$",
    )

    @field_validator("x_current_version")
    @classmethod
    def check_version(cls, v: str) -> str:
        def to_tuple(version: str) -> tuple[int, ...]:
            return tuple(map(int, version.split(".")))

        if to_tuple(v) < to_tuple(MINIMUM_APP_VERSION):
            raise ValueError("Требуется обновить приложение")
        return v
