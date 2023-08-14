from fastapi import FastAPI

from src.flats.router import router as flats_router


app = FastAPI(
    title="REST API проекта по поиску жилья"
)
app.include_router(flats_router)
