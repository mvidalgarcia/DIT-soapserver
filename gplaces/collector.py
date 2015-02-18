__author__ = 'Marco Vidal Garcia'

import sched
import time
import gplaces

s = sched.scheduler(time.time, time.sleep)


def launch_gplaces_collector():
    one_day_seconds = 24*60*60
    six_hours_seconds = 6*60*60
    while 1:
        #s.enter(5, 1, print_time, kwargs={'a': 'argumento'})
        s.enter(10, 1, gplaces.collect_one_place_each_category)
        s.run()


if __name__ == '__main__':
    launch_gplaces_collector()
