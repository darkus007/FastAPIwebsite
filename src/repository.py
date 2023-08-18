"""
Паттерн Репозиторий.

Модуль содержит абстрактный Репозиторий
и написанный на его основе SQLAlchemyRepository не привязанный к конкретной модели.
"""

from abc import ABC, abstractmethod

from sqlalchemy import insert, select, update
from sqlalchemy.ext.asyncio import AsyncSession


class AbstractRepository(ABC):
    @abstractmethod
    def __init__(self, session: AsyncSession):
        ...

    @abstractmethod
    async def add_one(self, data: dict):
        ...

    @abstractmethod
    async def patch_one(self, id: dict, data: dict):
        ...

    @abstractmethod
    async def delete_one(self, id: dict):
        ...

    @abstractmethod
    async def find_all(self, filters: dict | None, limit: int, offset: int):
        ...


class SQLAlchemyRepository(AbstractRepository):
    model = None

    def __init__(self, session=None):
        self.session = session

    async def add_one(self, data: dict) -> dict:
        """
        Добавляет запись в БД.

        :param data: данные для записи в формате dict;
        :return: созданная запись в формате dict.
        """
        stmt = insert(self.model).values(**data).returning(self.model)
        res = await self.session.execute(stmt)
        # await self.session.commit()   # перенесено в Unit of Work
        return res.scalar_one()

    async def patch_one(self, filter: dict, data: dict) -> dict:
        """
        Находит запись в БД по фильтру (id) и обновляет ее.

        :param filter: id записи, которую меняем;
        :param data: новые данные;
        :return: обновленная запись.
        """
        stmt = update(self.model).values(**data).filter_by(**filter).returning(self.model)
        res = await self.session.execute(stmt)
        # await self.session.commit()   # перенесено в Unit of Work
        return res.scalar_one()

    async def delete_one(self, filter: dict) -> dict:
        """
        Находит запись в БД по фильтру (id) и удаляет ее.

        :param filter: id записи, которую меняем;
        :return: id удаленной записи.
        """
        stmt = select(self.model).filter_by(**filter)
        res = await self.session.execute(stmt)
        obj = res.scalar_one()
        await self.session.delete(obj)
        return {}

    async def find_all(self, filters: dict | None = None, limit: int = 50, offset: int = 0) -> list[dict]:
        """
        Возвращает список объектов по заданным фильтрам.

        :param filters: фильтры в формате dict[поле модели: значение];
        :param limit: максимальное количество;
        :param offset: смещение от начала;
        :return: список словарей list[dict].
        """
        stmt = select(self.model).limit(limit).offset(offset=offset)
        if filters:
            stmt = stmt.filter_by(**filters)
        res = await self.session.execute(stmt)
        res = [row[0].to_dict() for row in res.all()]
        return res
