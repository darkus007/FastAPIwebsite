import uuid

from fastapi import FastAPI
from fastapi_users import FastAPIUsers

from src.flats.router import router as flats_router
from src.auth.config import auth_backend
from src.auth.models import User
from src.auth.services import get_user_manager
from src.auth.schemas import UserRead, UserCreate, UserUpdate


app = FastAPI(
    title="REST API проекта по поиску жилья"
)

# Роутеры для аутентификации
# https://fastapi-users.github.io/fastapi-users/12.1/configuration/routers/auth/
fastapi_users = FastAPIUsers[User, uuid.UUID](
    get_user_manager,
    [auth_backend],
)

app.include_router(
    fastapi_users.get_auth_router(auth_backend),
    prefix="/auth/jwt",
    tags=["Auth"],
)

app.include_router(
    fastapi_users.get_register_router(UserRead, UserCreate),
    prefix="/auth",
    tags=["Auth"],
)

app.include_router(
    fastapi_users.get_verify_router(UserRead),
    prefix="/auth",
    tags=["Auth"],
)

app.include_router(
    fastapi_users.get_reset_password_router(),
    prefix="/auth",
    tags=["Auth"],
)

app.include_router(
    fastapi_users.get_users_router(UserRead, UserUpdate),
    prefix="/users",
    tags=["Users"],
)

# Роутеры приложения flats
app.include_router(flats_router)
