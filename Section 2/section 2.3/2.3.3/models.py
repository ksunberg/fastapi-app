from pydantic import BaseModel, EmailStr, Field, ConfigDict, validator


bad_words = ["редиска", "редиски", "редиску", "редиской", "редиске",
             "бяка", "бяки", "бяку", "бякой", "бяке",
             "козявка", "козявки", "козявку", "козявкой", "козявке"]

pattern = "^(?!.*(" + "|".join(bad_words) + ")).*$"
class Contact(BaseModel):
    email: EmailStr
    phone: str
    @validator('phone')
    def validator_phone(cls, v):
        for k in v:
            if k not in '1234567890':
                raise ValueError('В номере телефона должны быть только цифры')
        return v

class Feedback(BaseModel):
    model_config = ConfigDict(regex_engine='python-re')
    username: str = Field(..., min_length=2, max_length=50, pattern = pattern)
    message: str = Field(..., min_length=10, max_length=500)
    contact: Contact

