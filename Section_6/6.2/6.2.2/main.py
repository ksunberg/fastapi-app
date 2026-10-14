from fastapi import FastAPI, Request, status
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from models import UserCreate, UserResponse, ProblemDetails

app = FastAPI()


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    errors = []
    for error in exc.errors():
        field = ".".join(str(loc) for loc in error["loc"])
        errors.append({
            "field": field,
            "message": error["msg"],
            "code": error["type"]
        })
    problem = ProblemDetails(
        instance=request.url.path,
        errors=errors
    )
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content=problem.dict(),
        media_type="application/problem+json"
    )

@app.post("/users", response_model=UserResponse)
async def create_user(user: UserCreate):
    return UserResponse(id=1, username=user.username)
