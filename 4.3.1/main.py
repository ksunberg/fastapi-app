from fastapi import FastAPI, HTTPException, Depends, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from datetime import datetime, timedelta
from typing import List
import jwt
from models import User, UserCreate, Resource, Role

app = FastAPI(
    title="RBAC API",
    description="API с управлением доступом на основе ролей",
    version="1.0.0"
)

security = HTTPBearer()

SECRET_KEY = "your-secret-key-here-2024"
ALGORITHM = "HS256"

users = {
    "admin": User(username="admin", password="admin123", role=Role.ADMIN),
    "user": User(username="user", password="user123", role=Role.USER),
    "guest": User(username="guest", password="guest123", role=Role.GUEST)
}

resources = []
next_id = 1


def create_token(username: str, role: Role) -> str:
    payload = {
        "username": username,
        "role": role.value,
        "exp": datetime.utcnow() + timedelta(minutes=30)
    }
    return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)


def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)):
    if not credentials:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Требуется авторизация"
        )

    try:
        token = credentials.credentials
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return {"username": payload["username"], "role": Role(payload["role"])}
    except jwt.ExpiredSignatureError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Токен истек"
        )
    except jwt.InvalidTokenError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Невалидный токен"
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"Ошибка авторизации: {str(e)}"
        )


def require_roles(allowed_roles: List[Role]):
    def check(current_user=Depends(get_current_user)):
        if current_user["role"] not in allowed_roles:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"Доступ запрещен. Требуется роль: {', '.join([r.value for r in allowed_roles])}"
            )
        return current_user

    return check


@app.post("/login")
def login(username: str, password: str):
    try:
        user = users.get(username)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Пользователь не найден"
            )

        if user.password != password:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Неверный пароль"
            )

        token = create_token(username, user.role)
        return {
            "access_token": token,
            "token_type": "bearer",
            "role": user.role.value,
            "username": username
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Ошибка сервера: {str(e)}"
        )


@app.get("/protected")
def protected(current_user=Depends(get_current_user)):
    return {
        "message": f"Привет {current_user['username']}",
        "role": current_user["role"].value,
        "timestamp": datetime.utcnow().isoformat()
    }


@app.get("/admin-only")
def admin_only(current_user=Depends(require_roles([Role.ADMIN]))):
    return {
        "message": "Административная панель",
        "users": list(users.keys()),
        "resources_count": len(resources)
    }


@app.post("/resources")
def create_resource(
        resource: Resource,
        current_user=Depends(require_roles([Role.ADMIN, Role.USER]))
):
    global next_id
    new_resource = {
        "id": next_id,
        "title": resource.title,
        "content": resource.content,
        "owner": current_user["username"],
        "created_at": datetime.utcnow().isoformat()
    }
    resources.append(new_resource)
    next_id += 1
    return new_resource


@app.get("/resources")
def get_resources(
        current_user=Depends(require_roles([Role.ADMIN, Role.USER, Role.GUEST]))
):
    if current_user["role"] == Role.ADMIN:
        return resources
    return [r for r in resources if r["owner"] == current_user["username"]]


@app.put("/resources/{resource_id}")
def update_resource(
        resource_id: int,
        resource: Resource,
        current_user=Depends(require_roles([Role.ADMIN, Role.USER]))
):
    for r in resources:
        if r["id"] == resource_id:
            if current_user["role"] != Role.ADMIN and r["owner"] != current_user["username"]:
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail="Нет прав на редактирование этого ресурса"
                )
            r["title"] = resource.title
            r["content"] = resource.content
            r["updated_at"] = datetime.utcnow().isoformat()
            return r
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="Ресурс не найден"
    )


@app.delete("/resources/{resource_id}")
def delete_resource(
        resource_id: int,
        current_user=Depends(require_roles([Role.ADMIN]))
):
    for i, r in enumerate(resources):
        if r["id"] == resource_id:
            resources.pop(i)
            return {"message": "Ресурс удален"}
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="Ресурс не найден"
    )


@app.get("/")
def root():
    return {
        "message": "RBAC API",
        "roles": [r.value for r in Role],
        "endpoints": {
            "POST /login": "Авторизация",
            "GET /protected": "Защищенный ресурс",
            "GET /admin-only": "Только для админа",
            "POST /resources": "Создать ресурс",
            "GET /resources": "Получить ресурсы",
            "PUT /resources/{id}": "Обновить ресурс",
            "DELETE /resources/{id}": "Удалить ресурс"
        }
    }