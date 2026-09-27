from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field, HttpUrl, field_validator


class CompanyBase(BaseModel):
    model_config = ConfigDict(str_strip_whitespace=True, extra="forbid")

    name: str = Field(min_length=1, max_length=200)
    website: HttpUrl | None = None
    notes: str | None = Field(default=None, max_length=5000)


class CompanyCreate(CompanyBase):
    pass


class CompanyRead(CompanyBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    created_at: datetime


class CompanyUpdate(BaseModel):
    model_config = ConfigDict(str_strip_whitespace=True, extra="forbid")

    name: str | None = Field(default=None, min_length=1, max_length=200)
    website: HttpUrl | None = None
    notes: str | None = Field(default=None, max_length=5000)

    @field_validator("name")
    @classmethod
    def name_not_null(cls, value: str | None) -> str | None:
        if value is None:
            raise ValueError("name cannot be null")
        return value
