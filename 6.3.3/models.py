from pydantic import BaseModel
from typing import Optional

class ErrorResponse(BaseModel):
    status_code: int
    message: str
    event_id: Optional[str] = None