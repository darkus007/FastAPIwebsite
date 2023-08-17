from fastapi import APIRouter, Depends

from src.flats.schemas import ProjectSchema, FlatSchema, PriceSchema
from src.flats.search_filters import project_filters, flat_filters, price_filters
from src.flats.services import ServiceFactory, Service

router = APIRouter(
    prefix="/housing",
    tags=["Housing"]
)


def pagination(limit: int = 50, offset: int = 0):
    return {"limit": limit, "offset": offset}


@router.get("/projects", response_model=list[ProjectSchema])
async def get_projects(
        project_filters: dict = Depends(project_filters),
        pagination: dict = Depends(pagination)
):
    return await ServiceFactory().project_service().get_all(project_filters, pagination)


@router.post("/projects")
async def add_project(project: ProjectSchema):
    return await ServiceFactory().project_service().add(project)


@router.get("/flats", response_model=list[FlatSchema])
async def get_flats(
        flat_filters: dict = Depends(flat_filters),
        pagination: dict = Depends(pagination)
):
    return await ServiceFactory().flat_service().get_all(flat_filters, pagination)


@router.get("/prices", response_model=list[PriceSchema])
async def get_prices(
        price_filters: dict = Depends(price_filters),
        pagination: dict = Depends(pagination)
):
    return await ServiceFactory().price_service().get_all(price_filters, pagination)
