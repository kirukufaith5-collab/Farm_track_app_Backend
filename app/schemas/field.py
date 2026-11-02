from datetime import datetime
from typing import List, Optional
from uuid import UUID

from pydantic import BaseModel, Field, field_validator


class Coordinate(BaseModel):
    lat: float = Field(..., ge=-90, le=90)
    lng: float = Field(..., ge=-180, le=180)


class FieldCreate(BaseModel):
    coordinates: List[Coordinate] = Field(..., min_length=3)
    farmer_code: Optional[str] = Field(None, max_length=64)
    owner_name: Optional[str] = Field(None, max_length=200)
    crop: Optional[str] = Field("Unassigned", max_length=120)
    notes: Optional[str] = Field(None, max_length=2000)
    area_ha: Optional[float] = Field(None, ge=0)

    @field_validator("coordinates")
    @classmethod
    def closed_ring_preferred(cls, v: List[Coordinate]) -> List[Coordinate]:
        # Frontend may or may not close the ring; we accept both.
        if len(v) < 3:
            raise ValueError("A polygon needs at least 3 points")
        return v


class FieldUpdate(BaseModel):
    coordinates: Optional[List[Coordinate]] = Field(None, min_length=3)
    farmer_code: Optional[str] = Field(None, max_length=64)
    owner_name: Optional[str] = Field(None, max_length=200)
    crop: Optional[str] = Field(None, max_length=120)
    notes: Optional[str] = Field(None, max_length=2000)
    area_ha: Optional[float] = Field(None, ge=0)


class FieldRead(BaseModel):
    id: UUID
    farmer_code: Optional[str] = None
    owner_name: Optional[str] = None
    crop: Optional[str] = None
    notes: Optional[str] = None
    area_ha: Optional[float] = None
    coordinates: List[Coordinate]
    centre_lat: Optional[float] = None
    centre_lng: Optional[float] = None
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}
