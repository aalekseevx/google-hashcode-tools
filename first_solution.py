from random import randint
from test import Solution, print_solutions
import random
from logging import getLogger
import sortedcontainers as s
logger = getLogger("Task.first_solution")

def sample_ans(input_):
    world, books, libraries = input_
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
        best_libs.add((sm, lib.id))

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


        
        win_id = best_libs[-1][1]
        # print (f"take library {win_id}")
        to_append = (win_id, [i[1] for i in to_scan[win_id]])
        # print(to_append)
        answer.append(to_append)
        for del_book in to_scan[win_id]:
            for where_lib in books_to_libs[del_book[1]]:
                try: 
                    to_scan[where_lib].remove((books[del_book[1]], del_book[1]))
                except KeyError:
                    pass

        best_libs.pop(-1)
        day += lib.signup
    return answer

solution = Solution(sample_ans, 1, "first_solution")
if __name__ == "__main__":
    print_solutions([solution])
