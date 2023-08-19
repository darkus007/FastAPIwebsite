"""
Настройка аутентификации.

Выбираем cookie транспорт
https://fastapi-users.github.io/fastapi-users/12.1/configuration/authentication/transports/cookie/

и jwt стратегию
https://fastapi-users.github.io/fastapi-users/12.1/configuration/authentication/strategies/jwt/

"""
from fastapi_users.authentication import (
    AuthenticationBackend,
    CookieTransport,
    JWTStrategy,
)

from src.config import settings

SECRET = settings.AUTH_SECRET


cookie_transport = CookieTransport(cookie_max_age=3600)


def get_jwt_strategy() -> JWTStrategy:
    return JWTStrategy(secret=SECRET, lifetime_seconds=3600)


auth_backend = AuthenticationBackend(
    name="jwt",
    transport=cookie_transport,
    get_strategy=get_jwt_strategy,
)
