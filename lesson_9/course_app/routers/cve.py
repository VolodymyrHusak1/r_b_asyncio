from typing import Annotated
from fastapi import APIRouter, Depends, Query, BackgroundTasks, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from ..deps import get_db_session
from ..schemas import CVERecord
from ..cron import cve_pull_scheduler
from ..crud import (_get_all_cve,
                    _search_cve_id,
                    _create_cve,
                    _load_cve,
                    _update_data)

cve_api = APIRouter(prefix="/cve")


@cve_api.get("/")
async def read_cves(db: Annotated[AsyncSession, Depends(get_db_session)],
                    cve_id: str | None = None,
                    title: str | None = None,
                    date_published: str | None = None,
                    date_updated: str | None = None,
                    limit: int = Query(10, ge=0),
                    offset: int = Query(0, ge=0)
                    ) -> list[CVERecord]:
    result = await _get_all_cve(db,
                                cve_id=cve_id,
                                title=title,
                                date_published=date_published,
                                date_updated=date_updated,
                                limit=limit,
                                offset=offset)

    return [CVERecord.model_validate(cve) for cve in result.fetchall()]


@cve_api.post("/")
async def create_cve(cve_record: CVERecord, db: Annotated[AsyncSession, Depends(get_db_session)]) -> CVERecord:
    record = await _create_cve(db, cve_record)
    await db.refresh(record)
    return CVERecord.model_validate(record)


@cve_api.get("/{cve_id}")
async def read_cve(cve_id: str, db: Annotated[AsyncSession, Depends(get_db_session)]) -> CVERecord:
    result = await _search_cve_id(db, cve_id)
    return CVERecord.model_validate(result.fetchone()[0])

@cve_api.patch("/")
async def read_cve(cve_record: CVERecord, db: Annotated[AsyncSession, Depends(get_db_session)]):
    record = await _update_data(db, cve_record.model_dump())
    if record:
        return {'message': 'ok'}
    raise HTTPException(status_code=404, detail="Item not found")

@cve_api.get("/reload_db")
async def reload_db(db: Annotated[AsyncSession, Depends(get_db_session)]):
    await _load_cve(db)
    return {'message': 'ok'}

@cve_api.get("/cve_scheduler")
async def cve_scheduler(db: Annotated[AsyncSession, Depends(get_db_session)],
                        background_tasks: BackgroundTasks):
    background_tasks.add_task(cve_pull_scheduler, db)

    return {'message': 'ok'}