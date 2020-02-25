from random import randint
from test import Solution, print_solutions
from random import shuffle
from logging import getLogger
logger = getLogger("Task.random_solution")

def sample_ans(input_):
    world, books, libraries = input_
    ans = []
    # print(f"Got w {world} b {books} l {libraries}")
    shuffle(libraries)
    for lib in libraries:
        lib_books = list(lib.books)
        shuffle(lib_books)
        ans.append( (lib.id, lib_books) )
    # print(f"Got ans {ans}")
    return ans


solution = Solution(sample_ans, 1, "random_solution")
if __name__ == "__main__":
    print_solutions([solution])
