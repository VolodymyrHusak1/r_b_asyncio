import asyncio
from contextvars import ContextVar


THINKERS_COUNT = 5
thinkers = ContextVar("thinkers")  # , default="unknown"
thinkers.set({})


async def eat(id):
    thinkers.get()[id] = False
    print(id, 'Eating..')
    await asyncio.sleep(1)
    print(id, 'End Eating')
    thinkers.get()[id] = True

async def thinker(id):
    while True:
        print(id, 'Thinking..')

        await asyncio.sleep(1)
        left = THINKERS_COUNT if id - 1 < 1 else id - 1
        right = 1 if id + 1 > THINKERS_COUNT else id + 1
        if thinkers.get().get(left, True) and thinkers.get().get(right, True):
            await eat(id)

async def main():
    tasks = []
    for i in range(1,6):
        task = asyncio.create_task(thinker(i))
        tasks.append(task)
    await asyncio.wait(tasks, timeout=10)


if __name__ == '__main__':
    asyncio.run(main())