from fastapi import FastAPI, Query, Header, Path, Body
from pydantic import BaseModel

app = FastAPI()


class ValueModel(BaseModel):
    value: str


@app.post("/data/{value_from_path}")
async def get_data(
        value_from_path: str = Path(),
        value_from_query: str = Query(None),
        value_from_body: ValueModel = Body(None),
        value_from_header: str = Header(None)
):
    res = []
    if value_from_body:
        res.append({"value": value_from_body.value, "source": "body"})
    if value_from_query:
        res.append({"value": value_from_query, "source": "query"})
    if value_from_header:
        res.append({"value": value_from_header, "source": "header"})
    if value_from_path:
        res.append({"value": value_from_path, "source": "path"})
    return res

