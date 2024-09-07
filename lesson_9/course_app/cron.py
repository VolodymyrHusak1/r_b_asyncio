import asyncio
import time
from .tools import pull_cve, _load_cve_delta, _get_cve_from_link, _dict_record_data
from .crud import _inster_data, _update_data


async def _parse_delta_cve(cves):
    res = []
    for cve in cves:
        cve_json = await _get_cve_from_link(cve['githubLink'])
        cve_record = _dict_record_data(cve_json)
        res.append(cve_record)
    return res

async def cve_pull_scheduler(db):
    print('cve_pull_scheduler')
    while True:
        pull_cve()
        cve_updated, cve_new = await _load_cve_delta()
        tasks = []
        cve_records_new = await _parse_delta_cve(cve_new)
        cve_records_updated = await _parse_delta_cve(cve_updated)
        tasks.append(asyncio.create_task(_inster_data(db, cve_records_new)))
        tasks.append(asyncio.create_task(_update_data(db, cve_records_updated)))
        time.sleep(60)
