from random import randint
from test import Solution, print_solutions
from logging import getLogger
logger = getLogger("Task.random_solution")

def sample_ans(input_):
    sm = 0
    ans = []
    for i, sl in enumerate(input_['pizza']):
        if sm + sl <= input_['M']:
            ans.append(i)
            sm += sl
    return ans

solution = Solution(sample_ans, 100, "random_solution")
if __name__ == "__main__":
    print_solutions([solution])
