"""
Паттерн Репозиторий

Абстрактный Репозиторий.
Предоставляет SQLAlchemyRepository не привязанный к конкретной модели.
"""

from abc import ABC, abstractmethod

from sqlalchemy import insert, select, update
from sqlalchemy.ext.asyncio import AsyncSession

from src.database import async_session


class AbstractRepository(ABC):
    @abstractmethod
    async def add_one(self, data: dict):
        ...

    @abstractmethod
    async def patch_one(self, id: int, data: dict):
        ...

    @abstractmethod
    async def find_all(self, filters: dict | None, limit: int, offset: int):
        ...


class SQLAlchemyRepository(AbstractRepository):
    model = None

    def __init__(self, session: AsyncSession = async_session()):
        self.session = session

    async def add_one(self, data: dict) -> int:
        stmt = insert(self.model).values(**data).returning(self.model.id)
        res = await self.session.execute(stmt)
        await self.session.commit()
        return res.scalar_one()

    async def patch_one(self, id: int, data: dict) -> int:
        stmt = update(self.model).values(**data).filter_by(id=id).returning(self.model.id)
        res = await self.session.execute(stmt)
        await self.session.commit()
        return res.scalar_one()

    async def find_all(self, filters: dict | None = None, limit: int = 50, offset: int = 0):
        stmt = select(self.model).limit(limit).offset(offset=offset)
        if filters:
            stmt = stmt.filter_by(**filters)
        res = await self.session.execute(stmt)
        res = [row[0].to_dict() for row in res.all()]
        return res
