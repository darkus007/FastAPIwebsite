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
    data_created: datetime = Field(default_factory=datetime.now)
    data_closed: Optional[datetime] = None


class ProjectPatchSchema(BaseModel):
    city: Optional[str] = Field(max_length=127, default=None)
    name: Optional[str] = Field(max_length=127, default=None)
    url: Optional[str] = Field(max_length=255, default=None)
    metro: Optional[str] = Field(max_length=127, default=None)
    time_to_metro: Optional[int] = None
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    address: Optional[str] = Field(max_length=255, default=None)
    data_closed: Optional[datetime] = None


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
    data_created: datetime = Field(default_factory=datetime.now)
    data_closed: Optional[datetime]


class FlatPatchSchema(BaseModel):
    project_id: Optional[int] = None
    address: Optional[str] = Field(max_length=255, default=None)
    floor: Optional[int] = None
    rooms: Optional[int] = None
    area: Optional[float] = None
    finishing: Optional[bool] = None
    bulk: Optional[str] = Field(max_length=127, default=None)
    settlement_date: Optional[datetime] = None
    url_suffix: Optional[str] = Field(max_length=127, default=None)
    data_closed: Optional[datetime] = None


class PriceSchema(BaseModel):
    price_id: int
    flat_id: int
    benefit_name: Optional[str] = Field(max_length=127)
    benefit_description: Optional[str] = Field(max_length=255)
    price: int
    meter_price: Optional[int]
    booking_status: Optional[str] = Field(max_length=15)
    data_created: datetime = Field(default_factory=datetime.now)


class PricePatchSchema(BaseModel):
    flat_id: Optional[int] = None
    benefit_name: Optional[str] = Field(max_length=127, default=None)
    benefit_description: Optional[str] = Field(max_length=255, default=None)
    price: Optional[int] = None
    meter_price: Optional[int] = None
    booking_status: Optional[str] = Field(max_length=15, default=None)
