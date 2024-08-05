import os
import argparse
import asyncio
import aiohttp
import aiofiles
import shutil

DATA_DIR_NAME = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'data_dir')
TIMEOUT = 10


def read_input_file(file_path):
    with open(file_path, 'r') as file:
        urls = file.readlines()
    return urls


def init(file_path):
    if os.path.exists(DATA_DIR_NAME):
        shutil.rmtree(DATA_DIR_NAME)
    os.mkdir(DATA_DIR_NAME)
    res = read_input_file(file_path)
    return res


async def save_to_file(path, data):
    path = os.path.join(DATA_DIR_NAME, path)
    async with aiofiles.open(path, 'wb') as file:
        await file.write(data)


async def load_url(url, session):
    try:
        async with session.get(f'https://{url}') as response:
            if response.status != 200:
                raise Exception('Got non-200 response!')
            async for chunk, _ in response.content.iter_chunks():
                await save_to_file(url, chunk)
                # data = await response.read()
                # await save_to_file(url, data)
    except Exception as e:
        pass
        print(e)


async def load_url_wait_for(url, session):
    await asyncio.wait_for(load_url(url, session), timeout=TIMEOUT)


async def get_all_wait_for(url_list, session):
    coros = []
    for url in url_list:
        url = url.strip()
        coro = asyncio.create_task(load_url_wait_for(url, session), name=url)
        coros.append(coro)

    res = await asyncio.gather(*coros, return_exceptions=True)
    for res in filter(lambda i: i[1], zip(coros, res)):
        print(f'{res[0].get_name()} end with: {res[0]._exception!r}')


async def get_all_wait(url_list, session):
    tasks = []
    for url in url_list:
        url = url.strip()
        tasks.append(asyncio.create_task(load_url(url, session), name=url))
    done, pending = await asyncio.wait(tasks, timeout=TIMEOUT)
    pending = ','.join([task.get_name() for task in pending if not task.done()])
    print(f'TimeoutError: {pending}')


async def get_all_as_completed(url_list, session):
    tasks = []
    for url in url_list:
        url = url.strip()
        tasks.append(asyncio.create_task(load_url(url, session), name=url))
    try:
        for r, task in zip(asyncio.as_completed(
                tasks,
                timeout=TIMEOUT), tasks):
            await r
    except asyncio.TimeoutError:
        pending = ','.join([task.get_name() for task in tasks if not task.done()])
        print(f'TimeoutError: {pending}')


async def main(urls):
    async with aiohttp.ClientSession() as session:
        await get_all_wait(urls, session)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('file_path')
    args = parser.parse_args()
    urls = init(args.file_path)
    asyncio.run(main(urls))
