import asyncio
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, insert, update
from sqlalchemy.sql.operators import or_
from itertools import batched
from .models import CVERecord
from .schemas import CVERecord as CVERecordSchema
from .tools import _get_batch_file
from .deps import get_settings
from .db import Base, get_engine


async def create_tables():
    engine = get_engine(get_settings())
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

async def drop_tables():
    engine = get_engine(get_settings())
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)


async def _get_all_cve(db: AsyncSession,
                       **kwargs
                       ):

    limit = kwargs.pop('limit')
    offset = kwargs.pop('offset')
    exprs = []
    for batch in batched(kwargs.items(), n=2):
        first, second = batch
        exprs.append(
            or_(getattr(CVERecord, first[0]) == first[1], getattr(CVERecord, second[0]) == second[1])
        )
    print(exprs)
    return await db.scalars(select(CVERecord).where(*exprs).limit(limit).offset(offset))


async def _search_cve_id(db: AsyncSession, cve_id: str):
    return await db.execute(
        select(CVERecord)
        .where(CVERecord.cve_id == str(cve_id))
    )


async def _create_cve(db: AsyncSession, cve_record: CVERecordSchema) -> CVERecord:
    record = CVERecord(**cve_record.model_dump())
    db.add(record)
    await db.commit()
    return record



async def _insert_batch(session, model, records):
    ids = await session.execute(
                insert(model).returning(model.id),
                records
            )
    return ids

async def _inster_data(session, cve_records):
    ids = await _insert_batch(session, CVERecord, cve_records)
    await session.commit()

async def _load_cve(db: AsyncSession):
    tasks = []
    await drop_tables()
    await create_tables()
    async for cve_records in _get_batch_file():
        tasks.append(asyncio.create_task(_inster_data(db, cve_records)))
    done, pending = await asyncio.wait(tasks)
    print(done)
    print(pending)
    await db.commit()

async def _update_data(session, cve_records):
    print('_update_data')
    for cve_record in cve_records:
        await session.execute(
            update(CVERecord).where(CVERecord.cve_id == cve_record['cve_id']),
            cve_record
        )