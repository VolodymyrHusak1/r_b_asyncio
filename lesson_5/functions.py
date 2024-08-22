import os
import multiprocessing as mp


def count_words(lines: list[str]):
    words = {}
    for line in lines:
        _word, _, match_count, _ = line.split("\t")
        if _word in words:
            words[_word] += int(match_count)
        else:
            words[_word] = int(match_count)
    return words


def mp_count_words(lines: list[str], counter, lock):
    # words_num = 0
    # step = 100
    words = {}
    for line in lines:
        _word, _, match_count, _ = line.split("\t")
        if _word in words:
            words[_word] += int(match_count)
        else:
            words[_word] = int(match_count)

        # monitoring
        # because of lock, this can slow down processing time
        #
        # words_num += 1
        # if words_num % step == 0:
        #     words_num = 0
        #         counter.value += step

    with lock:
        counter.value += len(lines)
    return words


def _chunk_count_words(file_name: str,
                       chunk_start: int,
                       chunk_end: int,
                       counter: int, lock) -> dict:
    words = {}
    start = chunk_start
    with open(file_name, mode="r") as f:
        f.seek(chunk_start)
        for i, line in enumerate(f):
            chunk_start += len(line)
            if chunk_start > chunk_end:
                break
            _word, _, match_count, _ = line.split("\t")
            if _word in words:
                words[_word] += int(match_count)
            else:
                words[_word] = int(match_count)
            if i % 100_000 == 0:
                with lock:
                    counter.value -= start - chunk_start
                    start = chunk_start
    return words


def get_file_chunks(
        file_name: str,
        max_cpu: int = 8,
) -> tuple[int, list[tuple[str, int, int]]]:
    """Split flie into chunks"""
    cpu_count = min(max_cpu, mp.cpu_count())

    file_size = os.path.getsize(file_name)
    chunk_size = file_size // cpu_count

    start_end = list()
    with open(file_name, mode="r+b") as f:

        def is_new_line(position):
            if position == 0:
                return True
            else:
                f.seek(position - 1)
                return f.read(1) == b"\n"

        def next_line(position):
            f.seek(position)
            f.readline()
            return f.tell()

        chunk_start = 0
        while chunk_start < file_size:
            chunk_end = min(file_size, chunk_start + chunk_size)

            while not is_new_line(chunk_end):
                chunk_end -= 1

            if chunk_start == chunk_end:
                chunk_end = next_line(chunk_end)

            start_end.append(
                (
                    file_name,
                    chunk_start,
                    chunk_end,
                )
            )

            chunk_start = chunk_end

    return cpu_count, start_end, file_size
