from fastapi import FastAPI, HTTPException, Header

app = FastAPI()

@app.get("/headers")
async def get_headers(
        user_agent: str = Header(None, alias="User-Agent"),
        accept_language: str = Header(None, alias="Accept-Language")
):
    if user_agent is None:
        raise HTTPException(
            status_code=400,
            detail="Отсутствует заголовок User-Agent"
        )
    if accept_language is None:
        raise HTTPException(
            status_code=400,
            detail="Отсутствует заголовок Accept-Language"
        )
    if (
            not accept_language or
            not any(c.isalpha() or
            c == '-'
                for c in accept_language.split(',')[0].strip())
    ):
        raise HTTPException(
            status_code=400,
            detail="Неверный формат заголовка Accept-Language. Ожидается формат: 'en-US,en;q=0.9,es;q=0.8'"
        )
    return {
        "User-Agent": user_agent,
        "Accept-Language": accept_language
    }