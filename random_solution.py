from random import randint
from test import Solution, print_solutions
import random
from logging import getLogger
logger = getLogger("Task.random_solution")

def sample_ans(input_):
    world, books, libraries = input_
    ans = []
    for lib in random.shuffle(libraries):
        ans.append( (lib.id, random.shuffle(list(lib.books))) )
    return ans


solution = Solution(sample_ans, 100, "random_solution")
if __name__ == "__main__":
    print_solutions([solution])
