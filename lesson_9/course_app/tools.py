import json
import os
from glob import iglob
from itertools import batched
from datetime import datetime
from .config import Settings

import aiofiles

BATCH_SIZE = 1000


def _update_record_data_uuid(ids, record):
    # print(f'Start update_record {len(record)}')
    for uuid, data in zip(ids, record):
        data['cve_id'] = uuid[0].hex


async def _get_batch_file():
    cve_path = os.path.join(Settings.cve_path, '**/CVE-*.json')  # 'cvelistV5/cves/**/CVE-*.json'
    for batch in batched(iglob(cve_path, recursive=True), n=BATCH_SIZE):
        yield await _get_raw_data(batch)


async def _get_raw_data(batch):
    cve_records = []
    for record in batch:
        async with aiofiles.open(record) as file:
            data = await file.read()
            record = json.loads(data)
            cve_record = _dict_record_data(record)
            cve_records.append(cve_record)
    return cve_records


def _dict_record_data(record):
    date_published = record['cveMetadata'].get('datePublished')
    date_published = datetime.strptime(date_published[:19], "%Y-%m-%dT%H:%M:%S") if date_published else None
    date_updated = datetime.strptime(record['cveMetadata']['dateUpdated'][:19], "%Y-%m-%dT%H:%M:%S")

    descriptions = record['containers']['cna'].get(
        'descriptions')
    descriptions = descriptions[0]['value'] if descriptions else None

    cve_id = record['cveMetadata']['cveId']
    cve_title = record['containers']['adp'][0]['title'] if record['containers'].get('adp') else None
    cve_record = {"cve_id": cve_id,
                  "title": cve_title,
                  'date_published': date_published,
                  'date_updated': date_updated,
                  'descriptions': descriptions, }
    return cve_record
