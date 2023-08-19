"""
Наборы схем, которые предоставляет библиотека fastapi-users.
При необходимости расширения, добавляет новые свойства в данном модуле.
"""

import uuid
from typing import Optional

from fastapi_users import schemas
from pydantic import BaseModel, Field


class ExtraUserFields(BaseModel):
    first_name: Optional[str] = Field(max_length=255, default=None)
    last_name: Optional[str] = Field(max_length=255, default=None)


class UserRead(ExtraUserFields, schemas.BaseUser[uuid.UUID]):
    pass


class UserCreate(ExtraUserFields, schemas.BaseUserCreate):
    pass


class UserUpdate(ExtraUserFields, schemas.BaseUserUpdate):
    pass
