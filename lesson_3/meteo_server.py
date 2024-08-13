import asyncio
import random
import time


def generate_data():
    return f'temp={random.uniform(-30, 40)}pressure={random.uniform(645, 815)}'


class MeteoServerProtocol(asyncio.Protocol):

    def connection_made(self, transport):
        peername = transport.get_extra_info('peername')
        print('Connection from {}'.format(peername))
        self.transport = transport
        self.queue = asyncio.Queue()
        self.task = asyncio.create_task(self.connection_task(transport))
        self.generate_data_task = asyncio.create_task(self.gen_data(transport))
        self.generate_data_task.cancel()

    def _switcher(self, command):
        if command == 'loop':
            if self.generate_data_task.cancelled():
                task = self.gen_data(self.transport)
                self.generate_data_task = asyncio.create_task(task)
        else:
            if not self.generate_data_task.cancelled():
                self.generate_data_task.cancel()
            data = generate_data()
            peername = self.transport.get_extra_info('peername')
            self.transport.write(f'{peername}:{data}'.encode())

    async def connection_task(self, transport):
        transport.write(b"Connect\n")
        while True:
            message = await self.queue.get()
            peername = self.transport.get_extra_info('peername')
            print(peername, message)
            self._switcher(message)
            await asyncio.sleep(1)
            self.queue.task_done()
        transport.close()

    async def gen_data(self, transport):
        while True:
            await asyncio.sleep(1)
            data = generate_data()
            peername = self.transport.get_extra_info('peername')
            transport.write(f'{peername}:{data}'.encode())

    def data_received(self, data):
        message = data.decode()
        self.queue.put_nowait(message)

    def eof_received(self):
        if self.transport.can_write_eof():
            self.transport.write_eof()

    def connection_lost(self, error):
        if not self.generate_data_task.done():
            self.generate_data_task.cancel()
        if not self.task.done():
            self.task.cancel()
        super().connection_lost(error)


async def main():
    loop = asyncio.get_running_loop()

    server = await loop.create_server(
        MeteoServerProtocol,
        '127.0.0.1', 8888)
    async with server:
        await server.serve_forever()


asyncio.run(main())
