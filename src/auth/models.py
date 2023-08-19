"""
Модуль содержит
модель пользователя и репозиторий (адаптер) для работы с пользователем.
"""

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi_users_db_sqlalchemy import SQLAlchemyUserDatabase
from fastapi_users.db import SQLAlchemyBaseUserTableUUID

from src.database import get_async_session, Base


class User(SQLAlchemyBaseUserTableUUID, Base):
    """
    Модель пользователя, которую предоставляет библиотека fastapi-users.
    При необходимости расширения, добавляет новые свойства тут.
    """
    pass


async def get_user_db(session: AsyncSession = Depends(get_async_session)):
    """
    Возвращает репозиторий SQLAlchemyUserDatabase для User.
    Позволяет читать, создавать и удалять пользователя ...
    """
    yield SQLAlchemyUserDatabase(session, User)
