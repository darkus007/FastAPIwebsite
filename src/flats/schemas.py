from typing import Optional
from datetime import datetime

from pydantic import BaseModel, Field


class ProjectSchema(BaseModel):
    project_id: int
    city: str = Field(max_length=127)
    name: str = Field(max_length=127)
    url: Optional[str] = Field(max_length=255)
    metro: Optional[str] = Field(max_length=127)
    time_to_metro: Optional[int]
    latitude: Optional[float]
    longitude: Optional[float]
    address: Optional[str] = Field(max_length=255)
    data_created: datetime
    data_closed: Optional[datetime]


class FlatSchema(BaseModel):
    flat_id: int
    project_id: int
    address: Optional[str] = Field(max_length=255)
    floor: Optional[int]
    rooms: Optional[int]
    area: Optional[float]
    finishing: Optional[bool]
    bulk: Optional[str] = Field(max_length=127)
    settlement_date: Optional[datetime]
    url_suffix: Optional[str] = Field(max_length=127)
    data_created: datetime
    data_closed: Optional[datetime]


class PriceSchema(BaseModel):
    price_id: int
    flat_id: int
    benefit_name: Optional[str] = Field(max_length=127)
    benefit_description: Optional[str] = Field(max_length=255)
    price: int
    meter_price: Optional[int]
    booking_status: Optional[str] = Field(max_length=15)
    data_created: datetime
