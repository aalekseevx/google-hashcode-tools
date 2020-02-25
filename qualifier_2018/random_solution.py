from random import randint
from test import Solution, print_solutions
from logging import getLogger
logger = getLogger("Task.random_solution")

def random_ans(input_):
    field, rides = input_
    ans = [[] for _ in range(field.cars)]
    for r in range(field.rides):
        ans[randint(0, field.cars - 1)].append(r)
    return ans

solution = Solution(random_ans, 100, "random_solution")
if __name__ == "__main__":
    print_solutions([solution])
