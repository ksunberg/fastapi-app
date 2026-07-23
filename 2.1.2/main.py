from fastapi import FastAPI
from fastapi.responses import FileResponse

app = FastAPI()


@app.get("/")
async def read_root():
    return FileResponse("index.html")


@app.get("/api/get-value")
async def get_value():
    return {"значение": 586}

