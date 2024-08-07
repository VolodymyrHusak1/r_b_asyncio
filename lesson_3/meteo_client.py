import asyncio
import random


class EchoClientProtocol(asyncio.Protocol):

    def __init__(self, message, on_con_lost):
        self.message = message
        self.on_con_lost = on_con_lost

    def connection_made(self, transport):
        self.task = asyncio.create_task(self.connection_task(transport))

    async def connection_task(self, transport):
        while True:
            message = random.choice(['loop', 'one'])
            print(f'Send {message}')
            transport.write(message.encode())
            await asyncio.sleep(5)

    def data_received(self, data):
        print('Data received: {!r}'.format(data.decode()))

    def connection_lost(self, exc):
        print('The server closed the connection')
        self.on_con_lost.set_result(True)


async def main():
    loop = asyncio.get_running_loop()

    on_con_lost = loop.create_future()
    message = random.choice(['loop', 'one'])
    message = 'loop'

    transport, protocol = await loop.create_connection(
        lambda: EchoClientProtocol(message, on_con_lost),
        '127.0.0.1', 8888)

    try:
        await on_con_lost
    finally:
        transport.close()


asyncio.run(main())
