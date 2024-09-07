import os
import json
import time
import subprocess
from glob import iglob
from itertools import batched
from datetime import datetime

import aiohttp

from .deps import get_settings

import aiofiles

BATCH_SIZE = 1000


def _update_record_data_uuid(ids, record):
    # print(f'Start update_record {len(record)}')
    for uuid, data in zip(ids, record):
        data['cve_id'] = uuid[0].hex


async def _get_batch_file():
    settings = get_settings()
    cve_path = os.path.join(settings.cve_path, '**/CVE-*.json')  # 'cvelistV5/cves/**/CVE-*.json'
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

def load_cve_repo():
    if not os.path.exists('cvelistV5'):
        subprocess.run(["git", "clone", "https://github.com/CVEProject/cvelistV5.git", "--depth", "1"])

def pull_cve():
    print('pull_cve')
    subprocess.run(['pwd'])
    subprocess.call(["cd", "cvelistV5", "&&","git", "pull"], shell=True)


async def _get_cve_from_link(url):
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            if response.status != 200:
                raise Exception('Got non-200 response!')
            text_data = await response.text()
            return json.loads(text_data)

async def _load_cve_delta():
    settings = get_settings()
    cve_delta_path = os.path.join(settings.cve_path, 'delta.json')
    async with aiofiles.open(cve_delta_path) as file:
        data = await file.read()
        record = json.loads(data)
        cve_updated = record.get('updated', [])
        cve_new = record.get('new', [])
    return cve_updated, cve_new


