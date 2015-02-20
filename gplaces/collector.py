__author__ = 'Marco Vidal Garcia'

import sched
import time
import sys
import gplaces

# if there is no argument, default value: 6hr
if len(sys.argv) != 2:
    schedule_period = 6*60*60
    print("Default period value: 6 hours")
else:
    schedule_period = float(sys.argv[1])*60*60

print("Schedule period established: %f hours (%f seconds)" % (schedule_period/60/60, schedule_period))
s = sched.scheduler(time.time, time.sleep)


def launch_gplaces_collector():
    while 1:
        #s.enter(5, 1, print_time, kwargs={'a': 'argumento'})
        s.enter(schedule_period, 1, gplaces.collect_one_place_each_category)
        s.run()


if __name__ == '__main__':
    launch_gplaces_collector()
