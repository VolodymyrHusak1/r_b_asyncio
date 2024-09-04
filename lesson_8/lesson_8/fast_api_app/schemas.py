from pydantic import BaseModel, ConfigDict


class CVERecord(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    cve_id: str
    title: str | None = None
