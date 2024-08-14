import asyncio
from asyncio import Semaphore


async def thinker(number, left_fork, right_fork, thinker_semaphore):
    async with thinker_semaphore:
        while True:
            print(number, 'Think...')
            await asyncio.sleep(1)
            print(number, 'End Think...')
            async with left_fork, right_fork:
                await eat(number)


async def eat(number):
    print(number, 'Eat...')
    await asyncio.sleep(1)
    print(number, 'Stop Eat...')




async def main():
    worker_count = 5
    thinker_semaphore = Semaphore(worker_count - 1)
    forks = [Semaphore() for _ in range(worker_count + 1)]
    tasks = []
    for i in range(worker_count):
        left_fork = forks[i]
        right_fork = forks[(i + 1) % worker_count]
        task = asyncio.create_task(thinker(i, left_fork, right_fork, thinker_semaphore))
        tasks.append(task)

    await asyncio.gather(*tasks)


if __name__ == '__main__':
    asyncio.run(main())