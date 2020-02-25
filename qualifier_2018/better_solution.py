import sortedcontainers as s
from utils import *
from test import Solution, print_solutions
from logging import getLogger
logger = getLogger("Task.better_solution")


def solve(input_, k=100):
    field, rides = input_
    drivers = {
        0: [i for i in range(field.cars)]
    }
    drivers_positions = [ (0, 0) for _ in range(field.cars) ]
    times = s.SortedSet([0])
    rides_by_time = s.SortedSet(rides, key=lambda r: r.start)
    answer = [[] for i in range(field.cars)]
    # print("begin")
    # print([i.id for i in rides_by_time])
    while len(times) > 0:
        t = times[0]
        times.pop(0)
        if t >= field.maxtime:
            break
        while len(rides_by_time) > 0 and (rides_by_time[0].finish - dist(rides_by_time[0].origin, rides_by_time[0].destination)) < t:
            rides_by_time.pop(0)
        for driver in drivers[t]:
            # FIX
            max_dist = 0
            ride_č = None
            real_free = -1
            current_pos = drivers_positions[driver]
            for i, ride in enumerate(rides_by_time):
                if i > k and ride_č is not None:
                    break
            
                # validation
                to_start_dist = dist(drivers_positions[driver], ride.origin)
                c_dist = dist(ride.origin, ride.destination)
                real_start_time = max(ride.start, t + c_dist)
                real_finish_time = real_start_time + c_dist

                if real_finish_time > ride.finish:
                    continue

                # FIX
                if dist(ride.origin, ride.destination) > max_dist:
                    max_dist = dist(ride.origin, ride.destination)
                    ride_č = ride
                    real_free = real_finish_time

            if ride_č is not None:
                rides_by_time.remove(ride_č)
                drivers_positions[driver] = ride_č.destination
                times.add(real_free)
                if drivers.get(real_free) is None:
                    drivers[real_free] = []
                drivers[real_free].append(driver)
                answer[driver].append(ride_č.id)
                # print(ride_č.id)
                # print("after remove")
                # print([i.id for i in rides_by_time])
    logger.info(f"Answer {answer}")
    return answer

solution = Solution(solve, 1, "better_solution")
if __name__ == "__main__":
    print_solutions([solution])
