"""
Модуль содержит логику проекта,
которая реализована в виде общего класса Service.

Конфигурация под конкретную задачу происходит через фабрику ServiceFactory.

"""
from pydantic import BaseModel

from src.unit_of_work import AbstractUnitOfWork, UnitOfWorkFactory


class Service:
    def __init__(self, unit_of_work: AbstractUnitOfWork):
        self.unit_of_work = unit_of_work

    async def add(self, data: BaseModel):
        data_dict = data.model_dump()
        async with self.unit_of_work:
            result = await self.unit_of_work.objects.add_one(data_dict)
            # await self.uow.commit()   # закомментировано для тестов при разработке
            return result

    async def get_all(self, filters: dict, pagination: dict):
        async with self.unit_of_work:
            return await self.unit_of_work.objects.find_all(
                filters=filters,
                limit=pagination["limit"],
                offset=pagination["offset"]
            )


class ServiceFactory:
    @staticmethod
    def project_service():
        return Service(UnitOfWorkFactory.projects())

    @staticmethod
    def flat_service():
        return Service(UnitOfWorkFactory.flats())

    @staticmethod
    def price_service():
        return Service(UnitOfWorkFactory.prices())
