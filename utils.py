from collections import namedtuple
from typing import List, Tuple
from itertools import tee, izip
import math
from logging import getLogger
logger = getLogger("Task.utils")

tasks = {
    'a': "a_example.txt",
    'b': "b_read_on.txt",
    'c': "c_incunabula.txt",
    'd': "d_tough_choices.txt",
    'e': "e_so_many_books.txt",
    'f': "f_libraries_of_the_world.txt"
}

World = namedtuple("World", ["books", "libraries", "days"])
Library = namedtuple("Library", ["id", "signup", "daily", "books"])

def pairwise(iterable):
    "s -> (s0,s1), (s1,s2), (s2, s3), ..."
    a, b = tee(iterable)
    next(b, None)
    return izip(a, b)

## IO   ##

def read_test(testfile: str):
    world = None
    books = []
    libraries = []
    with open(testfile, "r") as f:
        line1 = f.readline()
        world = World._make( map(int, line1.split()) )
        line2 = f.readline()
        for score in map(int, line2.split()):
            books.append(score)
        for i, line in enumerate(pairwise(f.readlines())):
            nums = map(int, line[0].split())
            book_set = map(int, line[1].split())
            libraries.append(Library._make( [ i, nums[1], nums[2], set(book_set) ] ))
    return world, books, libraries


def write_answer(ans, answerfile: str):
    with open(answerfile) as f:
        f.writeline(f"{len(ans)}")
        for lib_id, books in ans:
            f.writeline(f"{lib_id} {len(books)}\n{' '.join(books)}")


## Score  ##

def score(input_, answer) -> int:
    world, books, libraries = input_
    current_time = 0
    score = 0
    scanned = set()
    for lib_id, books in answer:
        current_time += libraries[lib_id].signup
        if current_time >= world.days:
            break
        library = libraries[lib_id]
        scan_time = min(world.days - current_time, math.ceil(len(books) / library.daily))
        scanned_books = min(library.daily * scan_time, len(books))
        for book in books[:scanned_books]:
            scanned.add(book)
    for book in scanned:
        score += books[book]
    return score
