import asyncio
from asyncio import Lock
from asyncio import Event
lock = Lock()

class Worker:

    def __init__(self, ):
        self.index = None
        self.left_fork = None
        self.right_fork = None

    async def think(self, number, left_fork, right_fork):
        task = asyncio.create_task(self.eat(number, left_fork, right_fork))
        while True:
            print(number, 'think...')
            await asyncio.sleep(1)
            if not left_fork.is_set() and not right_fork.is_set():
                right_fork.set()
                left_fork.set()


            # await self.eat(number, left_fork, right_fork)
                # print([i.is_set() for i in forks])
            print(number, 'End think')

    async def eat(self, number, left_fork, right_fork):
        await left_fork.wait()
        await right_fork.wait()
        print(number, 'Eating..')
        left_fork.clear()
        right_fork.clear()
        await asyncio.sleep(1)
        print(number, 'End Eating')
        # print([i.is_set() for i in forks])


async def main():
    worker_count = 5
    forks = [Event() for _ in range(worker_count + 1)]
    worker = Worker()
    tasks_think = []
    for i in range(worker_count):
        left_fork = forks[i]
        right_fork = forks[(i + 1) % worker_count]
        tasks_think.append(asyncio.create_task(worker.think(i, left_fork, right_fork)))

    await asyncio.gather(*tasks_think)


if __name__ == '__main__':
    asyncio.run(main())
