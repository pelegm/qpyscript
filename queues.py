"""
.. queues.py
"""

## Framework
import Queue


class PushQueue(Queue.Queue):
    def push(self, item, block=True, timeout=None):
        """ Push an *item* into the queue.

        If optional args *block* is ``True`` and *timeout* is None (the
        default), block if necessary until a free slot is available. If
        *timeout* is a positive number, it blocks at most *timeout* seconds and
        if no free slot was available within that time, it gets the next
        available item out of the queue and tries again.

        Otherwise (*block* is ``False``), put an item on the queue if a free
        slot is immediately available, else it gets the next available item out
        of the queue and tries again (*timeout* is ignored in that case). """
        while True:
            try:
                self.put(item, block=block, timeout=timeout)

            except Queue.Full:
                try:
                    self.get_nowait()
                except Queue.Empty:
                    pass

            else:
                break

    def push_nowait(self, item):
        """ Equivalent to ``push(item, False)``. """
        self.push(item, False)
