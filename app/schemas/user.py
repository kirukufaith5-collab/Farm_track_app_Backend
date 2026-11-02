from datetime import datetime
from typing import Optional
from uuid import UUID

from pydantic import BaseModel, EmailStr, Field, field_validator
import re


class UserRegister(BaseModel):
    email: EmailStr
    phone: str = Field(..., min_length=7, max_length=32)
    password: str = Field(..., min_length=8, max_length=128)
    full_name: Optional[str] = Field(None, max_length=200)

    @field_validator("phone")
    @classmethod
    def normalize_phone(cls, v: str) -> str:
        # Keep digits, +, and leading spaces stripped
        cleaned = re.sub(r"[^\d+]", "", v.strip())
        if len(cleaned) < 7:
            raise ValueError("Phone number is too short")
        return cleaned


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class UserRead(BaseModel):
    id: UUID
    email: EmailStr
    phone: str
    full_name: Optional[str] = None
    is_active: bool
    created_at: datetime

    model_config = {"from_attributes": True}


class UserUpdate(BaseModel):
    full_name: Optional[str] = Field(None, max_length=200)
    phone: Optional[str] = Field(None, min_length=7, max_length=32)
