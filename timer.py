"""
.. timer.py

Various (threaded) timers.
"""

## Framework
import threading as th

## Time management
import datetime as dt
import datetools as dtt
import time

## Default number of iterations
inf = float('inf')


class CTimer(th.Thread):
    def __init__(self, interval, start=dtt.START_TIME, name=None,
                 iterations=inf, dtfunc=dt.datetime.now, daemon=True):

        ## Initialize thread
        th.Thread.__init__(self, name=name)
        self.daemon = daemon

        ## Iteration and time initialization
        self.interval = dt.timedelta(seconds=interval)
        self.rounder = dtt.datetime_rounder(delta=self.interval, start=start)
        self.iterations = iterations
        self.dtfunc = dtfunc

        self._stop_flag = False

    def sleep(self, interval):
        time.sleep(max(0, interval))

    def stop(self):
        self._stop_flag = True

    def do(self):
        pass

    def run(self):
        counter = 0
        while counter < self.iterations:
            now = self.dtfunc()
            delta = self.rounder(now) + self.interval - now
            self.sleep(delta.total_seconds())
            self.do()
            counter += 1

            if self._stop_flag:
                self.iterations = 0


class FuncCTimer(CTimer):
    def __init__(self, function, args=None, kwargs=None, **ctimer_kwargs):
        super(FuncCTimer, self).__init__(**ctimer_kwargs)
        self.function = function
        self.args = args or ()
        self.kwargs = kwargs or {}

    def do(self):
        self.function(*self.args, **self.kwargs)

