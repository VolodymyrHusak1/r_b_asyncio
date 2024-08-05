import os
import argparse
import asyncio
import aiohttp
import aiofiles
import shutil

DATA_DIR_NAME = 'data_dir'
TIMEOUT = 10


def parse_url(urls):
    return urls.split(',')

def read_input_file(file_path):
    with open(file_path, 'r') as file:
        urls = file.readlines()
    return urls

def init(file_path):
    shutil.rmtree(DATA_DIR_NAME)
    if not os.path.exists(DATA_DIR_NAME):
        os.mkdir(DATA_DIR_NAME)
    res = read_input_file(file_path)
    return res

async def save_to_file(path, data):
    # print('start save file', path)
    path = os.path.join('data_dir', path)
    async with aiofiles.open(path, 'wb') as file:
        await file.write(data)
    # print('end save file', path)

async def load_url(url, session):
    # print('start get url', url)
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
        # print(e)
    # print('end get url', url)


async def load_url_wait_for(url, session):
    await asyncio.wait_for(load_url(url, session), timeout=TIMEOUT)


async def get_all_wait_for(url_list, session):
    coros = []
    for url in url_list:
        url = url.strip()
        coro = asyncio.create_task(load_url_wait_for(url, session), name=url)
        coros.append(coro)

    res = await asyncio.gather(*coros, return_exceptions=True)
    print('pending', len(list(filter(lambda i: i[1], zip(coros, res)))))
    # for res in filter(lambda i: i[1], zip(coros, res)):
    #     print(f'Loading {res[0].get_name()} end with: {res[0]._exception!r}')


async def get_all_wait(url_list, session):
    tasks = []
    for url in url_list:
        url = url.strip()
        tasks.append(asyncio.create_task(load_url(url, session), name=url))
    done, pending = await asyncio.wait(tasks, timeout=TIMEOUT)
    print('done', len(done))
    print('pending', len(pending))

async def main(urls):
    async with aiohttp.ClientSession() as session:
        await get_all_wait(urls * 5, session)



if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('file_path')
    args = parser.parse_args()
    urls = init(args.file_path)
    asyncio.run(main(urls))