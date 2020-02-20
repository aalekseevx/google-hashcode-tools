from collections import namedtuple
from tabulate import tabulate
from typing import List, Tuple
from utils import tasks, score, read_test, write_answer
from glob import glob
from importlib import import_module
import os
import copy
import logging
from logging import getLogger
logger = getLogger("Task.test")

Solution = namedtuple("Solution", ["func", "iterations", "name"])
solutions: List[Solution] = []

def register_solution(solution):
    global solutions
    if not solution: return
    print(f"Register {solution}")
    solutions.append(solution)

def update_best(task, score, ans):
    files = glob(f"best/{task}@*@.txt")
    logger.debug(f"Have files for {files}")
    if len(files) == 0 or int(files[0].split('@')[1]) < score:
        if len(files) > 0:
            os.remove(files[0])
        write_answer(ans, f"best/{task}@{score}@.txt")

def get_best():
    total = 0
    results = []
    for task in tasks.values():
        files = glob(f"best/{task}@*@.txt")
        score = int(files[0].split('@')[1]) if len(files) != 0 else 0
        results.append(score)
        total += score
    results.append(total)
    return results

def check_solutions(solutions_: List[Solution], tasks: List[str]) -> List[List[int]]:
    def check(task, func, input_, iterations):
        max_score = 0
        for _ in range(iterations):
            max_score = max(max_score, test(task, func, input_))
        return max_score

    results = []
    for solution in solutions_:
        curr_result = []
        total = 0
        for task in tasks:
            input_ = read_test(task)
            sc = check(task, solution.func, input_, solution.iterations)
            total += sc
            curr_result.append(sc)
        curr_result.append(total)
        results.append(curr_result)
    return results

def test(task, solution, input_):
    ans = solution(copy.deepcopy(input_))
    sc = score(copy.deepcopy(input_), ans)
    update_best(task, sc, ans)
    return sc


def load_solutions():
    files = glob("*_solution.py")
    for file in files:
        register_solution(import_module(file[:-3]).solution)

def print_solutions(solutions_):
    prepare_logger()
    results = check_solutions(solutions_, list(tasks.values()))
    headers = [ "Solution" ] + list(tasks.keys()) + [ "Total" ]
    data = [ [ solutions_[i].name ] + r for i, r in enumerate(results) ]
    data.append([ "BEST" ] + get_best())
    print(tabulate(data, headers=headers))

def prepare_logger():
    simple_formatter = logging.Formatter('%(levelname)-8s %(name)-24s: %(message)s')
    debuglog = logging.StreamHandler()
    debuglog.setLevel(logging.WARNING)
    debuglog.setFormatter(simple_formatter)

    master_logger = logging.getLogger('Task')
    master_logger.setLevel(logging.DEBUG)

    master_logger.addHandler(debuglog)

if __name__ == "__main__":
    load_solutions()
    print_solutions(solutions)
