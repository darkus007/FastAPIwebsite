"""
Модуль содержит логику проекта,
которая реализована в виде общего класса Service.

Конфигурация под конкретную задачу происходит через фабрику ServiceFactory.

"""
from pydantic import BaseModel
from fastapi import HTTPException
from sqlalchemy.exc import NoResultFound, IntegrityError

from src.unit_of_work import AbstractUnitOfWork, UnitOfWorkFactory


class Service:
    def __init__(self, unit_of_work: AbstractUnitOfWork):
        self.unit_of_work = unit_of_work

    async def add(self, data: BaseModel):
        data_dict = data.model_dump()
        async with self.unit_of_work:
            try:
                result = await self.unit_of_work.objects.add_one(data_dict)
                await self.unit_of_work.commit()
                return result
            except IntegrityError:
                self.__raise_integrity_error()

    async def patch(self, filters: dict, data: BaseModel):
        async with self.unit_of_work:
            try:
                data_dict = data.model_dump(exclude_defaults=True)
                result = await self.unit_of_work.objects.patch_one(filters, data_dict)
                await self.unit_of_work.commit()
                return result
            except NoResultFound:
                self.__raise_not_found_error(filters)
            except IntegrityError:
                self.__raise_integrity_error()

    async def delete(self, filters: dict):
        async with self.unit_of_work:
            try:
                await self.unit_of_work.objects.delete_one(filters)
                await self.unit_of_work.commit()
                list_dict_items = list(filters.items())
                return {
                    "detail": {
                        "status": "success",
                        "details": f"Item with {list_dict_items[0][0]} = {list_dict_items[0][1]} removed."
                    }
                }
            except NoResultFound:
                self.__raise_not_found_error(filters)

    async def get_all(self, filters: dict, pagination: dict):
        async with self.unit_of_work:
            return await self.unit_of_work.objects.find_all(
                filters=filters,
                limit=pagination["limit"],
                offset=pagination["offset"]
            )

    @staticmethod
    def __raise_not_found_error(filters: dict):
        list_dict_items = list(filters.items())
        raise HTTPException(status_code=404,
                            detail={
                                "status": "error",
                                "details": f"{list_dict_items[0][0]} = {list_dict_items[0][1]} not found."
                            })

    @staticmethod
    def __raise_integrity_error():
        raise HTTPException(status_code=400,
                            detail={
                                "status": "error",
                                "details": "Check the data. Perhaps the reason is in 'id'."
                            })


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
