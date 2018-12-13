import naive
from generator import generate_puzzle, random_erase_grid, display

from multiprocessing import Process, Queue
import time


def _run_solve_process(width, height, grid, result_queue: Queue):
    try:
        result = naive.solve(width, height, grid)
    except:
        pass
    else:
        result_queue.put((width, height, grid, result))


def _run_generate_process(width, height, result_queue):
    try:
        grid = generate_puzzle(width, height)
        random_erase_grid(width, height, grid, 4)
    except:
        pass
    else:
        result_queue.put((width, height, grid))


def solve_many(*grid_pars):
    result_queue = Queue()

    jobs = [Process(
        target=_run_solve_process,
        args=(width, height, grid, result_queue)
    ) for width, height, grid in grid_pars]

    for job in jobs:
        job.start()

    while True:
        time.sleep(0.5)
        if any(not job.is_alive() for job in jobs):
            time.sleep(0.1)
            break

    for job in jobs:
        if job.is_alive():
            job.terminate()

    results = []
    while not result_queue.empty():
        result = result_queue.get()
        if all(result[3]):
            results.append(result)

    return results


def generate_many(width, height, k):
    result_queue = Queue()

    jobs = [Process(
        target=_run_generate_process,
        args=(width, height, result_queue)
    ) for _ in range(k)]

    for job in jobs:
        job.start()

    while True:
        time.sleep(0.2)
        if any(not job.is_alive() for job in jobs):
            time.sleep(0.1)
            break

    for job in jobs:
        if job.is_alive():
            job.terminate()

    results = []
    while not result_queue.empty():
        result = result_queue.get()
        results.append(result)

    return results


def main():
    width = height = 5

    many = generate_many(width, height, 5)
    result = solve_many(*many)
    print(result)
    print(len(result))


if __name__ == '__main__':
    before = time.time()
    main()
    print(time.time() - before)

    # grid = generate_puzzle(width, height)
    # random_erase_grid(width, height, grid, 5)
    # print(grid)
    # display(width, height, grid)
    #
    # grid = naive.solve(width, height, grid)
    # print(grid)
    # display(width, height, grid)
