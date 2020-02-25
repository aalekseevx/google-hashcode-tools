from random import randint
from test import Solution, print_solutions
import random
from logging import getLogger
import sortedcontainers as s
from copy import deepcopy
logger = getLogger("Task.constant_solution")

# iterations_av = 170
# K = 1000
disable_after = 100
# er = 9
random.seed(None)
magic = 7000
magic_2 = random.random()
magic = random.randint(0, 15000)
disable_after = random.randint(0, 200)

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
        about = 10000
        shift = 500
        a = random.randint(about - shift, about + shift)
        # [10000 - 500, 10000 + 500]
        best_libs.add((magic_2 * sm - magic * lib.signup, lib.id))

    day = 0
    # print(best_libs)
    iter = 0
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
                score -= magic_2 * price
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

        iter += 1
        if iter == disable_after:
            for score, id in best_libs:
                best_libs.remove((score, id))
                new_score = score + magic * libraries[id].signup
                best_libs.add((new_score, id))
    print(f"iteration: {iter}")
    return answer

solution = Solution(sample_ans, 20, "constant_solution")
if __name__ == "__main__":
    print_solutions([solution])
