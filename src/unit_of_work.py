"""
Паттерн Unit of Work.
Создает и закрывает сессию, управляет транзакциями.

Модуль содержит абстрактный Unit of Work (AbstractUnitOfWork)
и на его основе UnitOfWork не привязанный к конкретному репозиторию.

Фабрику UnitOfWorkFactory для создания UnitOfWork с требуемым репозиторием.
"""

from abc import ABC, abstractmethod

from src.database import async_session
from src.flats.repository import ProjectRepository, FlatRepository, PriceRepository
from src.repository import AbstractRepository


class AbstractUnitOfWork(ABC):
    objects: AbstractRepository

    @abstractmethod
    def __init__(self):
        ...

    @abstractmethod
    async def __aenter__(self):
        ...

    @abstractmethod
    async def __aexit__(self, *args):
        ...

    @abstractmethod
    async def commit(self):
        ...

    @abstractmethod
    async def rollback(self):
        ...


class UnitOfWork(AbstractUnitOfWork):
    def __init__(self, repository: AbstractRepository):
        self.session_factory = async_session
        self.objects = repository

    async def __aenter__(self):
        self.session = self.session_factory()
        self.objects.session = self.session

    async def __aexit__(self, *args):
        await self.rollback()
        await self.session.close()

    async def commit(self):
        await self.session.commit()

    async def rollback(self):
        await self.session.rollback()


class UnitOfWorkFactory:
    @staticmethod
    def projects():
        return UnitOfWork(ProjectRepository())

    @staticmethod
    def flats():
        return UnitOfWork(FlatRepository())

    @staticmethod
    def prices():
        return UnitOfWork(PriceRepository())
