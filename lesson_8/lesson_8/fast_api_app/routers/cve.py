from typing import Annotated
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from ..deps import get_db_session
from ..models import CVERecord as CVERecordModel
from ..schemas import CVERecord


cve_api = APIRouter(prefix="/cve")

@cve_api.get("/")
async def read_cves( db: Annotated[AsyncSession, Depends(get_db_session)]) -> list[CVERecord]:
    result = await db.execute(
        select(CVERecordModel.cve_id, CVERecordModel.title)
    )
    return [CVERecord.model_validate(cve) for cve in result.fetchall()]

@cve_api.get("/{cve_id}")
async def read_cve(cve_id: int, db: Annotated[AsyncSession, Depends(get_db_session)]) -> CVERecord:
    result = await db.execute(
        select(CVERecordModel)
        .where(CVERecordModel.cve_id==str(cve_id))
    )
    return CVERecord.model_validate(result.fetchone()[0])

@cve_api.post("/")
async def create_cve(cve_rocord: CVERecord, db: Annotated[AsyncSession, Depends(get_db_session)]) -> CVERecord:
    im = CVERecordModel(**cve_rocord.model_dump())
    db.add(im)
    await db.commit()

    # would not work wihout the refresh
    # refresh the instance to get the default values (pk, etc.)
    await db.refresh(im)
    return CVERecord.model_validate(im)
