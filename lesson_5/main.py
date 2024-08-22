import asyncio
import time
import multiprocessing as mp
from contextlib import contextmanager
from itertools import batched
from concurrent.futures import ProcessPoolExecutor
from functions import mp_count_words, get_file_chunks, _chunk_count_words


FILE_PATH = "./googlebooks-eng-all-1gram-20120701-a"
WORD = "ära"


@contextmanager
def timer(msg: str):
    start = time.perf_counter()
    yield
    print(f"{msg} took {time.perf_counter() - start:.2f} seconds")


def reduce_words(target: dict, source: dict) -> dict:
    for key, value in source.items():
        if key in target:
            target[key] += value
        else:
            target[key] = value
    return target


async def monitoring(counter, total):
    interval_seconds = 0.2  # can be adjusted

    while True:
        print(f"Progress: {counter.value}/{total}")
        if counter.value == total:
            break
        await asyncio.sleep(interval_seconds)


async def main():
    loop = asyncio.get_event_loop()

    words = {}

    cpu_count, chunks, file_size = get_file_chunks(FILE_PATH)
    # return
    with mp.Manager() as manager:
        counter = manager.Value("i", 0)
        counter_lock = manager.Lock()

        monitoring_task = asyncio.shield(
            asyncio.create_task(monitoring(counter, file_size))
        )

        with ProcessPoolExecutor(max_workers=cpu_count) as executor:
            with timer("Processing data"):
                results = []
                get_file_chunks(FILE_PATH)
                for file_name, chunk_start, chunk_end in chunks:
                    results.append(
                        loop.run_in_executor(
                            executor,
                            _chunk_count_words,
                            *(file_name, chunk_start, chunk_end),
                            counter,
                            counter_lock,
                        )
                    )

                done, _ = await asyncio.wait(results)

        monitoring_task.cancel()

    with timer("Reducing results"):
        for result in done:
            words = reduce_words(words, result.result())

    with timer("Printing results"):
        print("Total words: ", len(words))
        print("Total count for word : ", words[WORD])


if __name__ == "__main__":
    with timer("Total time"):
        asyncio.run(main())
    # print()