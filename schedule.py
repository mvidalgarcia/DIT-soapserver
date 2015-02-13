__author__ = 'Marco Vidal Garcia'

import sched
import time

s = sched.scheduler(time.time, time.sleep)
print("HEHEHE")

def print_time(a='default'):
    print("This is print_time function", time.time(), a)


def print_weird_things():
    while 1:
        print(time.time())
        s.enter(5, 1, print_time, kwargs={'a': 'holyshit2'})
        s.enter(5, 2, print_time, kwargs={'a': 'holyshit1'})
        s.enter(5, 5, print_time, kwargs={'a': 'holyshit the best'})
        s.enter(6, 1, print_time, kwargs={'a': 'holyshit3'})
        s.enter(10, 1, print_time, kwargs={'a': 'holyshit4'})
        s.enter(5, 4, print_time, kwargs={'a': 'theholyshiter'})
        s.run()

print_weird_things()
