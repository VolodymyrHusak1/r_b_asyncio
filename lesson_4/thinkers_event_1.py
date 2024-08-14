import asyncio
from asyncio import Event, Lock

lock = Lock()

worker_count = 5
forks = [Event() for _ in range(worker_count + 1)]

class Worker:

    def __init__(self, ):
        self.index = None
        self.left_fork = None
        self.right_fork = None

    async def think(self, number, left_fork, right_fork):
        while True:
            print(number, 'think...')
            await asyncio.sleep(1)
            if not left_fork.is_set() and not right_fork.is_set():
                left_fork.set()
                right_fork.set()
                print(number, 'set')
                # print([i.is_set() for i in forks])

            print(number, 'End think')

    async def eat(self, number, left_fork, right_fork):
        while True:
            await left_fork.wait()
            await right_fork.wait()
            print(number, 'Eating..')
            await asyncio.sleep(1)
            left_fork.clear()
            right_fork.clear()
            print(number, 'End Eating')
            # print([i.is_set() for i in forks])


async def main():

    worker = Worker()
    tasks_think = []
    tasks_eat = []
    for i in range(worker_count):
        left_fork = forks[i]
        right_fork = forks[(i + 1) % worker_count]
        tasks_think.append(asyncio.create_task(worker.think(i, left_fork, right_fork)))
        tasks_eat.append(asyncio.create_task(worker.eat(i, left_fork, right_fork)))

    await asyncio.gather(*tasks_eat)
    await asyncio.gather(*tasks_think)


if __name__ == '__main__':
    asyncio.run(main())
