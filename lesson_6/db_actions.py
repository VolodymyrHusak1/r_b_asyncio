import asyncio
from sqlalchemy import insert, select
from sqlalchemy.orm import joinedload
from models import CVERecord, CVERecordData, Base
from contextlib import asynccontextmanager
from typing import AsyncGenerator
from tools import timer
from config import config
from file_loading import _get_batch_file

from sqlalchemy.ext.asyncio import (
    create_async_engine,
    AsyncEngine,
    AsyncSession,
    async_sessionmaker,
)

def engine():
    return create_async_engine(
        config['DB_URI'],
        echo=False,
    )

@asynccontextmanager
async def make_session(
    engine: AsyncEngine,
) -> AsyncGenerator[AsyncSession, None]:
    session_factory = async_sessionmaker(engine)
    async with session_factory() as session:
        yield session

def _update_record_data_uuid(ids, record):
    # print(f'Start update_record {len(record)}')
    for uuid, data in zip(ids, record):
        data['cve_id'] = uuid[0].hex

async def _insert_batch(session, model, records):
    # with timer('_insert_batch'):
        # print(f'Start insert {model}, {len(records)}')
        ids = await session.execute(
                    insert(model).returning(model.id),
                    records
                )
        # print(f'End insert {model}, {len(records)}')
        return ids

async def create_tables():
    async with engine().begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

async def drop_tables():
    async with engine().begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)

async def _inster_data(session, cve_records, cve_records_data):
    with timer('_inster_data'):
        ids = await _insert_batch(session, CVERecord, cve_records)
        _update_record_data_uuid(ids, cve_records_data)
        ids = await _insert_batch(session, CVERecordData, cve_records_data)
        # print('commit')
        await session.commit()

async def load_cve():
    # logger.info("Hello, World!")
    await drop_tables()
    await create_tables()
    tasks = []
    with timer('main'):
        async with make_session(engine()) as session:
            async for batch in _get_batch_file():
                cve_records, cve_records_data = batch
                tasks.append(asyncio.create_task(_inster_data(session, cve_records, cve_records_data)))


            done, pending = await asyncio.wait(tasks)
            print(done)
            print(pending)
            await session.commit()


async def search_by_id(cve_id):
    async with make_session(engine()) as session:
        result = await session.execute(
            select(CVERecordData)
            .join(CVERecordData.cve)
            .where(CVERecord.cve_id == cve_id)
            .options(joinedload(CVERecordData.cve))
        )
        row = result.one()[0]
        print(row.cve)
        print(row)

async def search_by_date(date_published=None, date_updated=None):
    async with make_session(engine()) as session:
        result = await session.execute(
            select(CVERecordData)
            .join(CVERecordData.cve)
            .where(CVERecordData.date_published == date_published)
            .where(CVERecordData.date_updated == date_updated)
            .options(joinedload(CVERecordData.cve))
        )

        row = result.one()[0]
        print(row.cve)
        print(row)
