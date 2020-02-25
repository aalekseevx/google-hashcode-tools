from random import randint
from test import Solution, print_solutions
import random
from logging import getLogger
import sortedcontainers as s
from copy import deepcopy
logger = getLogger("Task.third_solution")

def sample_ans(input_):
    world, books, libraries = input_
    about = 15000   # e - 15000
    shift = 1000
    const = random.randint(about - shift, about + shift)
    best_libs = s.SortedSet(key=lambda x: x[0])
    answer = []
    books_to_libs = [[] for _ in range(world.books)]
    to_scan = [s.SortedSet(key=lambda x: x[0]) for _ in range(world.libraries)]
    for lib in libraries:
        sm = 0
        for book in lib.books:
            to_scan[lib.id].add((books[book], book))
            sm += books[book]
            books_to_libs[book].append(lib.id)
        # [10000 - 500, 10000 + 500]
        best_libs.add((sm - const * lib.signup, lib.id))

    day = 0
    # print(best_libs)
    while len(best_libs) > 0 and day < world.days:
        def update_lib():
            lib_id = best_libs[-1][1]
            lib = libraries[lib_id]
            score = best_libs[-1][0]
            time_left = (world.days - day - lib.signup) * lib.daily
            was_hit = False
            best_libs.pop(-1)

            # print (f'Upd lib {lib_id}. Books left {time_left}')
            while len(to_scan[lib_id]) > max(0, time_left):
                price, item = to_scan[lib_id][0]
                score -= price
                to_scan[lib_id].pop(0)
                was_hit = True
            # print(f"final score {score}")
            best_libs.add((score, lib_id))
            return was_hit

        while update_lib():
            pass

        def use_lib(my_id):
            lib = libraries[my_id]
            # print (f"take library {win_id}")
            to_append = deepcopy((my_id, [i[1] for i in to_scan[my_id]]))
            # print(to_append)
            if len(to_append) > 0:
                answer.append(to_append)
            for del_book in to_scan[my_id]:
                for where_lib in books_to_libs[del_book[1]]:
                    try: 
                        to_scan[where_lib].remove((books[del_book[1]], del_book[1]))
                    except KeyError:
                        pass

        win_id = best_libs[-1][1]
        use_lib(win_id)
        lib = libraries[win_id]
        day += lib.signup
        best_libs.pop(-1)
    return answer

solution = Solution(sample_ans, 20, "third_solution")
if __name__ == "__main__":
    print_solutions([solution])
