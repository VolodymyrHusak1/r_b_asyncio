import uuid
from pydantic import BaseModel, ConfigDict
from pydantic import BaseModel, field_validator, validator

class OrmBase(BaseModel):
    # Common properties across orm models
    id: uuid.UUID

    class Config:
        orm_mode = True

class CVERecord(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    cve_id: str
    title: str | None = None
    date_published: str | None = None
    date_updated: str | None = None
    descriptions: str | None = None
