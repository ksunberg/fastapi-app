from pydantic import BaseModel, validator
from fastapi import Header

class CommonHeaders(BaseModel):
    user_agent: str = Header(..., alias="User-Agent")
    accept_language: str = Header(..., alias="Accept-Language")

    @validator('accept_language')
    def validate_accept_language(cls, v):
        parts = v.split(',')
        for part in parts:
            part = part.strip()
            if ';q=' in part:
                lang, q = part.split(';q=')
                if not lang or not q:
                    raise ValueError('Неверный формат Accept-Language')
                try:
                    q_value = float(q)
                    if q_value < 0 or q_value > 1:
                        raise ValueError('q-значение должно быть от 0 до 1')
                except ValueError:
                    raise ValueError('Неверный формат q-значения')
            else:
                if not part:
                    raise ValueError('Неверный формат Accept-Language')
        return v

    class Config:
        allow_population_by_field_name = True