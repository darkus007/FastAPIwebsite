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
    def __init__(self):
        self.session_factory = async_session

    async def __aenter__(self):
        self.session = self.session_factory()

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
        uow_projects = UnitOfWork()
        uow_projects.objects = ProjectRepository(session=uow_projects.session_factory)
        return uow_projects

    @staticmethod
    def flats():
        uow_flats = UnitOfWork()
        uow_flats.objects = FlatRepository(session=uow_flats.session_factory)
        return uow_flats

    @staticmethod
    def prices():
        uow_prices = UnitOfWork()
        uow_prices.objects = PriceRepository(session=uow_prices.session_factory)
        return uow_prices
