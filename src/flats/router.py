from fastapi import APIRouter, Depends
from sqlalchemy import select

from src.database import async_session
from src.flats.models import Project, Flat, Price
from src.flats.schemas import ProjectSchema, FlatSchema, PriceSchema
from src.flats.repository import ProjectRepository, FlatRepository, PriceRepository
from src.flats.search_filters import project_filters

router = APIRouter(
    prefix="/flats",
    tags=["Flats"]
)


def pagination(limit: int = 50, offset: int = 0):
    return {"limit": limit, "offset": offset}


@router.get("/projects", response_model=list[ProjectSchema])
async def get_projects(
        project_filter: dict = Depends(project_filters),
        pagination: dict = Depends(pagination)
):
    return await ProjectRepository().find_all(
        filters=project_filter,
        limit=pagination["limit"],
        offset=pagination["offset"]
    )


@router.get("/flats", response_model=list[FlatSchema])
async def get_flats(pagination: dict = Depends(pagination)):
    return await FlatRepository().find_all(limit=pagination["limit"], offset=pagination["offset"])


@router.get("/prices", response_model=list[PriceSchema])
async def get_flats(pagination: dict = Depends(pagination)):
    return await PriceRepository().find_all(limit=pagination["limit"], offset=pagination["offset"])
