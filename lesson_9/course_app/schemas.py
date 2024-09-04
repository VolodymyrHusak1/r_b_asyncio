
from pydantic import BaseModel, ConfigDict
from datetime import datetime


class CVERecord(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    cve_id: str
    title: str | None = None
    date_published: datetime | None = None
    date_updated: datetime | None = None
    descriptions: str | None = None
