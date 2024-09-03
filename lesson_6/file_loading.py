import os
import json
import aiofiles
from glob import iglob
from datetime import datetime
from itertools import batched
from config import config

BATCH_SIZE = 1000


async def _get_batch_file():
    cve_path = os.path.join(config['filename'], '**/CVE-*.json') # 'cvelistV5/cves/**/CVE-*.json'
    for batch in batched(iglob(cve_path, recursive=True), n=BATCH_SIZE):
        yield await _get_raw_data(batch)


async def _get_raw_data(batch):
    cve_records = []
    cve_records_data = []
    for record in batch:
        async with aiofiles.open(record) as file:
            data = await file.read()
            record = json.loads(data)
            cve_record, cve_data = _dict_record_data(record)
            cve_records.append(cve_record)
            cve_records_data.append(cve_data)
    return cve_records, cve_records_data



def _dict_record_data(record):
    date_published = record['cveMetadata'].get('datePublished')
    date_published = datetime.strptime(date_published[:19], "%Y-%m-%dT%H:%M:%S") if date_published else None
    date_updated = datetime.strptime(record['cveMetadata']['dateUpdated'][:19], "%Y-%m-%dT%H:%M:%S")

    descriptions = record['containers']['cna'].get(
        'descriptions')
    descriptions = descriptions[0]['value'] if descriptions else None


    cve_data = {
        'date_published': date_published,
        'date_updated': date_updated,
        'descriptions': descriptions,
    }

    cve_id = record['cveMetadata']['cveId']
    cve_title = record['containers']['adp'][0]['title'] if record['containers'].get('adp') else None
    cve_record = { "cve_id": cve_id, "title": cve_title}
    return cve_record, cve_data