#!/usr/bin/python

'''
Created on Mar 20, 2011

@author: Daniel Underwood
'''


# symmetric implementation of dining philosophers

import sys
import threading
import time

class ChopStick:
    def __init__(self, number):
        self.number = number           # chop stick ID
        self.user = -1                 # keep track of philosopher using it
        self.lock = threading.Lock()
    
    def get_lock(self):
        return self.lock

    def take(self, user):         # just for I/O, not used for synchronization
        if self.user == -1:
            self.user = user
            sys.stdout.write("p[%s] took c[%s]\n" % (user, self.number))
        else:
            sys.stdout.write("p[%s] cannot take c[%s] (taken by c[%s])\n" % 
                             (user, self.number, self.user))
            sys.exit(1)

    def drop(self, user):         # just for I/O, not used for synchronization
        if self.user == user:
            self.user = -1
            sys.stdout.write("p[%s] dropped c[%s]\n" % (user, self.number))
        else:
            sys.stdout.write("p[%s] cannot drop c[%s] (taken by c[%s])\n" % 
                             (user, self.number, self.user))
            sys.exit(1)


class Philosopher (threading.Thread):
    def __init__(self, number, left, right):
        threading.Thread.__init__(self)
        self.number = number            # philosopher number
        self.left = left
        self.right = right

    def run(self):
        for i in range(20):
            time.sleep(0.1)             # think
            with self.left.get_lock():
                self.left.take(self.number)
#                time.sleep(0.1)         # yield makes deadlock more likely
                with self.right.get_lock():
                    self.right.take(self.number)
                    time.sleep(0.1)     # eat
                    self.right.drop(self.number)
                self.left.drop(self.number)
        sys.stdout.write("p[%s] finished thinking and eating\n" % self.number)


def main():
    # number of philosophers / chop sticks
    n = 5

    # list of chopsticks
    c = [ChopStick(i) for i in range(n)]

    # list of philsophers
    p = [Philosopher(i, c[i], c[(i + 1) % n]) for i in range(n)]

    for i in range(n):
        p[i].start()


if __name__ == "__main__":
    main()
