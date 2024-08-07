import asyncio
import random

HOST = 'localhost'
PORT = 8888


async def client_reader() -> None:
    reader, writer = await asyncio.open_connection(HOST, PORT)

    writer.write(b'start')
    await writer.drain()

    while True:
        data = await reader.read(1024)
        if reader.at_eof():
            print('Socket Closed')
            break
        print(data.decode())

    writer.close()
    await writer.wait_closed()


if __name__ == '__main__':
    loop = asyncio.new_event_loop()
    loop.run_until_complete(client_reader())
