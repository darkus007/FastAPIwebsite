"""
Наборы схем, которые предоставляет библиотека fastapi-users.
При необходимости расширения, добавляет новые свойства в данном модуле.
"""

import uuid

from fastapi_users import schemas


class UserRead(schemas.BaseUser[uuid.UUID]):
    pass


class UserCreate(schemas.BaseUserCreate):
    pass


class UserUpdate(schemas.BaseUserUpdate):
    pass
