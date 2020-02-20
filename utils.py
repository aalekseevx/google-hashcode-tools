from collections import namedtuple
from typing import List, Tuple
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
    a = next(iterable)
    b = next(iterable, None)
    return (a, b)

## IO   ##

def read_test(testfile: str):
    world = None
    books = []
    libraries = []
    with open(testfile, "r") as f:
        line1 = f.readline()
        world = World._make( map(int, line1.split()) )
        # print(f"World {world}")
        line2 = f.readline()
        for score in map(int, line2.split()):
            books.append(score)
        # print(f"Book scores {books}")
        i = 0
        while line1 := f.readline():
            line2 = f.readline()
            if not line1 or not line2:
                break
            lib_info = list(map(int, line1.split()))
            book_set = set(list(map(int, line2.split())))
            new_library = Library._make( [ i, lib_info[1], lib_info[2], book_set ] )
            # print(f"Library {new_library}")
            libraries.append(new_library)
            i += 1
    return world, books, libraries


def write_answer(ans, answerfile: str):
    with open(answerfile, 'w') as f:
        f.write(f"{len(ans)}\n")
        for lib_id, books in ans:
            f.write(f"{str(lib_id)} {len(books)}\n{' '.join(map(str,books))}\n")


## Score  ##

def score(input_, answer) -> int:
    world, books, libraries = input_
    # print(f"Got w {world} b {books} l {libraries}")
    current_time = 0
    score = 0
    scanned = set()
    for lib_id, ans_books in answer:
        current_time += libraries[lib_id].signup
        if current_time >= world.days:
            break
        library = libraries[lib_id]
        scan_time = min(world.days - current_time, math.ceil(len(ans_books) / library.daily))
        scanned_books_len = min(library.daily * scan_time, len(ans_books))
        scanned_books = ans_books[:scanned_books_len]
        # print(f"scanning {scanned_books}, lib books {library.books}")
        if not set(scanned_books) <= library.books:
            logger.error(f"Scanned books that are not in library")
        for book in scanned_books:
            scanned.add(book)
    # print(f"Got books {list(scanned)}\nglobal {books}")
    for book in scanned:
        score += books[book]
    return score
