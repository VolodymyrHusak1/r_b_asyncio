import asyncio
from asyncio import Event


class Worker:

    def __init__(self, ):
        self.index = None
        self.left_fork = None
        self.right_fork = None

    async def think(self, number, left_fork, right_fork):
        asyncio.create_task(self.eat(number, left_fork, right_fork))
        while True:
            await asyncio.sleep(1)
            print(number, 'think')
            if not left_fork.is_set() and not right_fork.is_set():
                left_fork.set()
                right_fork.set()
                # print([i.is_set() for i in forks])

    async def eat(self, number, left_fork, right_fork):
        while True:
            await left_fork.wait()
            await right_fork.wait()
            await asyncio.sleep(1)
            print(number, 'eat')
            # print([i.is_set() for i in forks])
            left_fork.clear()
            right_fork.clear()
            # print([i.is_set() for i in forks])


async def main():
    worker_count = 6
    forks = [Event() for i in range(worker_count + 1)]
    worker = Worker()
    tasks_think = []
    for i in range(worker_count):
        left_fork = forks[i]
        right_fork = forks[(i + 1) % worker_count]
        tasks_think.append(asyncio.create_task(worker.think(i, left_fork, right_fork)))

    await asyncio.gather(*tasks_think)


if __name__ == '__main__':
    asyncio.run(main())
