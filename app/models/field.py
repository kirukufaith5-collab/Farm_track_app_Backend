from datetime import datetime, timezone
from typing import TYPE_CHECKING, List, Optional
from uuid import UUID, uuid4

from geoalchemy2 import Geometry
from sqlalchemy import Column
from sqlmodel import Field, Relationship, SQLModel

if TYPE_CHECKING:
    from app.models.user import User


def utcnow() -> datetime:
    return datetime.now(timezone.utc)


class Field(SQLModel, table=True):
    """
    A farm parcel (polygon) owned by a user.

    Geometry is stored as PostGIS Polygon in EPSG:4326.
    Coordinates from the frontend arrive as [{lat, lng}, ...].
    """

    __tablename__ = "fields"

    id: UUID = Field(default_factory=uuid4, primary_key=True)
    user_id: UUID = Field(foreign_key="users.id", index=True)

    farmer_code: Optional[str] = Field(default=None, max_length=64, index=True)
    owner_name: Optional[str] = Field(default=None, max_length=200)
    crop: Optional[str] = Field(default="Unassigned", max_length=120)
    notes: Optional[str] = Field(default=None, max_length=2000)
    area_ha: Optional[float] = Field(default=None)

    # PostGIS polygon. Use sa_column so SQLModel does not treat it as a normal field.
    geom: Optional[str] = Field(
        default=None,
        sa_column=Column(
            Geometry(geometry_type="POLYGON", srid=4326, spatial_index=True),
            nullable=False,
        ),
    )

    centre_lat: Optional[float] = Field(default=None)
    centre_lng: Optional[float] = Field(default=None)

    created_at: datetime = Field(default_factory=utcnow)
    updated_at: datetime = Field(default_factory=utcnow)

    owner: Optional["User"] = Relationship(back_populates="fields")
