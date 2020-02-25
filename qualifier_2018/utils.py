from collections import namedtuple
from typing import List, Tuple
from logging import getLogger
logger = getLogger("Task.utils")

Field = namedtuple("Field", ["rows", "cols", "cars", "rides", "bonus", "maxtime"])
Ride  = namedtuple("Ride", ["origin", "destination", "start", "finish", "id"])
tasks = {
    'a': "a_example.in",
    'b': "b_should_be_easy.in",
    'c': "c_no_hurry.in",
    'd': "d_metropolis.in",
    'e': "e_high_bonus.in",
}


def dist(start: Tuple[int, int], finish: Tuple[int, int]) -> int:
    return abs(start[0] - finish[0]) + abs(start[1] - finish[1])


## IO   ##

def read_test(testfile: str) -> Tuple[Tuple, List[Tuple]]:
    field = None
    rides = []
    with open(testfile, "r") as f:
        field = Field._make(map(int, f.readline().split()))
        for i, ride in enumerate(f.readlines()):
            ride = ride.split()
            new_ride = Ride._make([ (int(ride[0]), int(ride[1])), (int(ride[2]), int(ride[3])), int(ride[4]), int(ride[5]), i ])
            rides.append(new_ride)
    return field, rides


def read_answer(answerfile: str, cars: int) -> List[List[int]]:
    ans = [[] for _ in range(cars)]
    with open(answerfile, "r") as f:
        for i, c in enumerate(f.readlines()):
            rides = c.split()
            ans[i] = map(int, rides[1:])
    return ans


def write_answer(ans: List[List[int]], answerfile: str):
    with open(answerfile, "w") as f:
        f.writelines([ f"{len(c)} { ' '.join([ str(r) for r in c ]) }\n" for c in ans ])


## Score  ##

def score(input_, answer) -> int:
    field, rides = input_
    done_rides = set()
    all_rides = set(range(field.rides))
    stats = { 'skipped_rides': set(), 'bonus_rides': 0 }
    score = 0
    for index, vehicle in enumerate(answer):
        current_time = 0
        current_pos = (0, 0)
        for ride_id in vehicle:
            ride = rides[ride_id]
            current_score = 0
            if ride in done_rides:
                logger.error(f"ERROR: two vehicles on ride #{ride_id} {ride}")
            done_rides.add(ride)
            logger.debug(f"Vehicle #{index} started ride #{ride_id} at {current_time}")
            current_time = max(current_time + dist(current_pos, ride.origin), ride.start)
            logger.debug(f"Vehicle #{index} reached ride #{ride_id} at {current_time}")
            if current_time == ride.start:
                current_score += field.bonus
                stats['bonus_rides'] += 1
            
            current_time += dist(ride.origin, ride.destination)
            logger.debug(f"Vehicle #{index} finished ride #{ride_id} at {current_time}")
            current_pos = ride.destination
            
            if current_time <= ride.finish:
                current_score += dist(ride.origin, ride.destination)
            else:
                logger.info(f"INFO: vehicle #{index} late on ride #{ride_id}")
            logger.info(f"Vehicle #{index} on ride #{ride_id} with score={current_score} and time={current_time}")
            score += current_score
    
    # stats['skipped_rides'] = all_rides.difference(done_rides)
    stats['skipped_rides'] = field.rides - len(done_rides)  # len(stats['skipped_rides'])
    logger.info(f"Total score {score}")
    logger.info(f"Stats: {stats}")
    return score
