import asyncio
import random

HOST = 'localhost'
PORT = 8888


def generate_data():
    return f'temp={random.uniform(-30, 40)}pressure={random.uniform(645, 815)}'


async def client_task(reader, writer):
    client_addr = writer.get_extra_info('peername')
    print(client_addr)
    try:

        while True:
            m = generate_data()
            writer.write(m.encode())
            await writer.drain()
            await asyncio.sleep(1)
    except Exception as e:
        print(e)

    writer.close()
    await writer.wait_closed()
    return


async def handler(reader: asyncio.StreamReader, writer: asyncio.StreamWriter) -> None:
    def client_cleanup(fu):
        try:
            fu.result()
            print(fu)
        except Exception:
            pass

    task = asyncio.ensure_future(client_task(reader, writer))
    task.add_done_callback(client_cleanup)



async def server_run() -> None:
    server = await asyncio.start_server(handler, HOST, PORT)
    async with server:
        print('Server Start')
        await server.serve_forever()


if __name__ == '__main__':
    loop = asyncio.new_event_loop()
    loop.run_until_complete(server_run())
