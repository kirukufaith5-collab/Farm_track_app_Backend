from datetime import datetime, timezone
from typing import List
from uuid import UUID

from fastapi import APIRouter, HTTPException, status
from sqlmodel import select

from app.api.deps import CurrentUser, SessionDep
from app.models.field import Field
from app.schemas.field import FieldCreate, FieldRead, FieldUpdate
from app.services.geometry import (
    coordinates_to_wkt_element,
    geom_to_coordinates,
    polygon_centre,
)

router = APIRouter(prefix="/fields", tags=["fields"])


def _to_read(field: Field) -> FieldRead:
    return FieldRead(
        id=field.id,
        farmer_code=field.farmer_code,
        owner_name=field.owner_name,
        crop=field.crop,
        notes=field.notes,
        area_ha=field.area_ha,
        coordinates=geom_to_coordinates(field.geom),
        centre_lat=field.centre_lat,
        centre_lng=field.centre_lng,
        created_at=field.created_at,
        updated_at=field.updated_at,
    )


@router.get("", response_model=List[FieldRead])
def list_fields(session: SessionDep, current_user: CurrentUser):
    rows = session.exec(
        select(Field)
        .where(Field.user_id == current_user.id)
        .order_by(Field.created_at.desc())
    ).all()
    return [_to_read(r) for r in rows]


@router.post("", response_model=FieldRead, status_code=status.HTTP_201_CREATED)
def create_field(
    payload: FieldCreate,
    session: SessionDep,
    current_user: CurrentUser,
):
    centre_lat, centre_lng = polygon_centre(payload.coordinates)
    field = Field(
        user_id=current_user.id,
        farmer_code=payload.farmer_code,
        owner_name=payload.owner_name,
        crop=payload.crop or "Unassigned",
        notes=payload.notes,
        area_ha=payload.area_ha,
        geom=coordinates_to_wkt_element(payload.coordinates),
        centre_lat=centre_lat,
        centre_lng=centre_lng,
    )
    session.add(field)
    session.commit()
    session.refresh(field)
    return _to_read(field)


@router.get("/{field_id}", response_model=FieldRead)
def get_field(field_id: UUID, session: SessionDep, current_user: CurrentUser):
    field = session.get(Field, field_id)
    if not field or field.user_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Field not found")
    return _to_read(field)


@router.patch("/{field_id}", response_model=FieldRead)
def update_field(
    field_id: UUID,
    payload: FieldUpdate,
    session: SessionDep,
    current_user: CurrentUser,
):
    field = session.get(Field, field_id)
    if not field or field.user_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Field not found")

    data = payload.model_dump(exclude_unset=True)
    coords = data.pop("coordinates", None)

    for key, value in data.items():
        setattr(field, key, value)

    if coords is not None:
        from app.schemas.field import Coordinate
        coord_objs = [Coordinate(**c) if isinstance(c, dict) else c for c in coords]
        field.geom = coordinates_to_wkt_element(coord_objs)
        field.centre_lat, field.centre_lng = polygon_centre(coord_objs)

    field.updated_at = datetime.now(timezone.utc)
    session.add(field)
    session.commit()
    session.refresh(field)
    return _to_read(field)


@router.delete("/{field_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_field(field_id: UUID, session: SessionDep, current_user: CurrentUser):
    field = session.get(Field, field_id)
    if not field or field.user_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Field not found")
    session.delete(field)
    session.commit()
    return None
