from fastapi import FastAPI
from models import Feedback

app = FastAPI()

feedbacks = []

@app.post("/feedback")
async def add_feedback(fb: Feedback):
    feedbacks.append(fb)
    return {"message": "Отзыв добавлен"}

@app.get("/feedback")
async def get_all_feedbacks():
    return {"feedbacks": feedbacks}