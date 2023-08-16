"""
Паттерн Репозиторий

Задаем модель для абстрактного репозитория
"""

from src.flats.models import Project, Flat, Price
from src.repository import SQLAlchemyRepository


class ProjectRepository(SQLAlchemyRepository):
    model = Project


class FlatRepository(SQLAlchemyRepository):
    model = Flat


class PriceRepository(SQLAlchemyRepository):
    model = Price
