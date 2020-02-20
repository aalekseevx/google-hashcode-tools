from collections import namedtuple
from typing import List, Tuple
from logging import getLogger
logger = getLogger("Task.utils")

tasks = {
    'a': "a_example.in",
    'b': "b_small.in",
    'c': "c_medium.in",
    'd': "d_quite_big.in",
    'e': "e_also_big.in",
}

## IO   ##

def read_test(testfile: str):
    with open(testfile, "r") as fin:
    	numbers = list(map(int, fin.read().split()))
    	M, N = numbers[0], numbers[1]
    	return {
    		"M": M,
    		"pizza": numbers[2:]
    	}


def write_answer(ans, answerfile: str):
    with open(answerfile, "w") as fout:
    	if (len(ans) < 100):
    		print(ans)
    	fout.write(f"{len(ans)}\n")
    	fout.write(" ".join(map(str, ans)))


## Score  ##

def score(input_, answer) -> int:
	ans = sum([input_['pizza'][i] for i in answer])
	if ans > input_['M']:
		logger.error("you lost")
		return 0
	else:
		return ans
