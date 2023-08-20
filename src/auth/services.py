"""
Логика работы с пользователями.

https://fastapi-users.github.io/fastapi-users/12.1/configuration/user-manager/
"""

import uuid
from typing import Optional

from fastapi import Depends, Request
from fastapi_users import BaseUserManager, FastAPIUsers, UUIDIDMixin

from fastapi_users.db import SQLAlchemyUserDatabase

from src.auth.config import auth_backend
from src.auth.models import User, get_user_db
from src.config import settings
from src.tasks.celery_tasks import send_email

SECRET = settings.AUTH_SECRET


class UserManager(UUIDIDMixin, BaseUserManager[User, uuid.UUID]):
    reset_password_token_secret = SECRET
    verification_token_secret = SECRET

    async def on_after_register(self, user: User, request: Optional[Request] = None):
        print(f"User {user.id} has registered.")
        # Выполняем метод request_verify, который генерирует токен
        # затем вызывает метод on_after_request_verify и передает ему токен
        await self.request_verify(user, request)

    async def on_after_forgot_password(
            self, user: User, token: str, request: Optional[Request] = None
    ):
        print(f"User {user.id} has forgot their password. Reset token: {token}")
        # Отправляем письмо для восстановления пароля
        send_email.delay(user.email, token, content="forgot_password")

    async def on_after_request_verify(
            self, user: User, token: str, request: Optional[Request] = None
    ):
        print(f"Verification requested for user {user.id}. Verification token: {token}")
        # Отправляем письмо для подтверждения e-mail
        send_email.delay(user.email, token)


async def get_user_manager(user_db: SQLAlchemyUserDatabase = Depends(get_user_db)):
    yield UserManager(user_db)


fastapi_users = FastAPIUsers[User, uuid.UUID](get_user_manager, [auth_backend])


# Пользователи для разграничения доступа в роутерах
# https://fastapi-users.github.io/fastapi-users/12.1/usage/current-user/

# авторизованный и активный (is_active) пользователь
current_active_user = fastapi_users.current_user(active=True)

# авторизованный, активный (is_active) и верифицированный (is_verified) пользователь
current_active_verified_user = fastapi_users.current_user(active=True, verified=True)

# авторизованный суперпользователь (is_superuser)
current_superuser = fastapi_users.current_user(active=True, superuser=True)
