from pydantic import BaseModel, ConfigDict, Field

bad_words = ["редиска", "редиски", "редиску", "редиской", "редиске",
             "бяка", "бяки", "бяку", "бякой", "бяке",
             "козявка", "козявки", "козявку", "козявкой", "козявке"]

pattern = "^(?!.*(" + "|".join(bad_words) + ")).*$"

# r используется для того чтобы не экранировать каждый слэш
# " просто сама строка пишется в кавычках
# ^ начать просмотр текста с первого же символа
# ?! проверка
# .* любое количество любых символов
# слова через или, то есть мат |(или) зло и тд
# .* любое количество любых символов
# $ дойди до последнего символа
print(pattern)

class Feedback(BaseModel):
    model_config = ConfigDict(regex_engine='python-re')
    username: str = Field(..., min_length=2, max_length=50, pattern=pattern)
    message: str = Field(..., min_length=10, max_length=500)



