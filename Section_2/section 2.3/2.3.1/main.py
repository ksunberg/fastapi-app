from fastapi import FastAPI
from models import Feedback

app = FastAPI()
feedbacks = []

@app.post("/feedback")
async def submit_feedback(feedback: Feedback):
    feedbacks.append(feedback)
    return {"message": f"Feedback received. Thank you, {feedback.name}."}


@app.get("/feedbacks")
async def get_feedbacks():
    return feedbacks

#переделать в базу данных и возвращать последние 3 запроса добавить входной параметр времени последнего запроса возвращаемого в ответе