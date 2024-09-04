from pydantic import BaseModel

class Settings(BaseModel):
    db_uri: str = "postgresql+asyncpg://odoo:odoo@localhost/course_app"
    cve_path: str = "cvelistV5/cves"

