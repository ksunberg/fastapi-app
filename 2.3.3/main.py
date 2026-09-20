from fastapi import FastAPI, Query
from models import Feedback

app = FastAPI()

feedbacks = []

@app.post("/feedback")
async def add_feedback(
        fb: Feedback,
        is_premium: bool = Query(False)
):
    feedbacks.append(fb)
    message = f"Спасибо, {fb.username}! Ваш отзыв сохранён."
    if is_premium:
        message += " Ваш отзыв будет рассмотрен в приоритетном порядке."
    return {"message": message}