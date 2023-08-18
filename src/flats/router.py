from fastapi import APIRouter, Depends

from src.flats.schemas import ProjectSchema, FlatSchema, PriceSchema
from src.flats.schemas import ProjectPatchSchema, FlatPatchSchema, PricePatchSchema
from src.flats.search_filters import project_filters, flat_filters, price_filters
from src.flats.services import ServiceFactory

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


@router.post("/projects", response_model=ProjectSchema)
async def add_project(project: ProjectSchema):
    return await ServiceFactory().project_service().add(project)


@router.patch("/projects", response_model=ProjectSchema)
async def patch_project(project_id: int, project: ProjectPatchSchema):
    return await ServiceFactory().project_service().patch({"project_id": project_id}, project)


@router.delete("/projects")
async def delete_project(project_id: int):
    return await ServiceFactory().project_service().delete({"project_id": project_id})


@router.get("/flats", response_model=list[FlatSchema])
async def get_flats(
        flat_filters: dict = Depends(flat_filters),
        pagination: dict = Depends(pagination)
):
    return await ServiceFactory().flat_service().get_all(flat_filters, pagination)


@router.post("/flats", response_model=FlatSchema)
async def add_flat(flat: FlatSchema):
    return await ServiceFactory().flat_service().add(flat)


@router.patch("/flats", response_model=FlatSchema)
async def patch_flat(flat_id: int, flat: FlatPatchSchema):
    return await ServiceFactory().flat_service().patch({"flat_id": flat_id}, flat)


@router.delete("/flats")
async def delete_flat(flat_id: int):
    return await ServiceFactory().flat_service().delete({"flat_id": flat_id})


@router.get("/prices", response_model=list[PriceSchema])
async def get_prices(
        price_filters: dict = Depends(price_filters),
        pagination: dict = Depends(pagination)
):
    return await ServiceFactory().price_service().get_all(price_filters, pagination)


@router.post("/prices", response_model=PriceSchema)
async def add_price(price: PriceSchema):
    return await ServiceFactory().price_service().add(price)


@router.patch("/prices", response_model=PriceSchema)
async def patch_price(price_id: int, price: PricePatchSchema):
    return await ServiceFactory().price_service().patch({"price_id": price_id}, price)


@router.delete("/prices")
async def delete_price(price_id: int):
    return await ServiceFactory().price_service().delete({"price_id": price_id})
