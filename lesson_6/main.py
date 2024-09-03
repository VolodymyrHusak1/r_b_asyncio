import logging
import asyncio
from datetime import datetime
from db_actions import load_cve, search_by_id, search_by_date
from config import init_config




logging.basicConfig(level=logging.INFO)
# logging.getLogger("sqlalchemy.engine").setLevel(logging.INFO)
logger = logging.getLogger(__name__)

async def main():
    await load_cve()
    await search_by_id("CVE-1999-0001")
    date_published = datetime.strptime('2000-02-04T05:00:00', "%Y-%m-%dT%H:%M:%S")
    date_updated = datetime.strptime('2024-08-01T16:03:04', "%Y-%m-%dT%H:%M:%S")
    await search_by_date(date_published=date_published, date_updated=date_updated)



if __name__ == '__main__':
    asyncio.run(main())