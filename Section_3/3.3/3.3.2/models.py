from pydantic import BaseModel, Field, field_validator


class CommonHeaders(BaseModel):
    user_agent: str = Field(alias="User-Agent")
    accept_language: str = Field(alias="Accept-Language")

    @field_validator("accept_language")
    @classmethod
    def validate_accept_language(cls, v: str) -> str:
        for part in (p.strip() for p in v.split(",")):
            if not part:
                raise ValueError("Неверный формат Accept-Language")
            if ";q=" in part:
                lang, _, q = part.partition(";q=")
                if not lang or not q:
                    raise ValueError("Неверный формат Accept-Language")
                try:
                    q_value = float(q)
                except ValueError:
                    raise ValueError("Неверный формат q-значения")
                if q_value < 0 or q_value > 1:
                    raise ValueError("q-значение должно быть от 0 до 1")
        return v
