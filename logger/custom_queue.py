import threading

class CustomQueue(object):
    """A priority queue that can return both oldest and youngest elements.

    Queue has no size limit.

    Public methods are thread safe.

    Priorities are given by the timestamps. The queue can return
    both the oldest and the youngest element (as implied by the
    timestamp).
    """

    def __init__(self):
        self._cv = threading.Condition()
        self._data = []

    def put(self, timestamp, kind, value):
        """Inserts one element into the queue."""
        with self._cv:
            self._data.append((timestamp, kind, value))
            self._sort_items()
            self._cv.notify(n=1)

    def get_youngest(self):
        """Retrieves one element from the queue (with largest timestamp).

        Blocks if there's no element.
        """
        with self._cv:
            while self._queue_empty():
                self._cv.wait()
            timestamp, kind, value = self._data.pop(-1)
            return timestamp, kind, value

    def get_youngest_nowait(self):
        """Retrieves one element from the queue (with largest timestamp).

        Returns None if the queue is empty.
        """
        with self._cv:
            if not self._data:
                return None
            timestamp, kind, value = self._data.pop(-1)
            return timestamp, kind, value

    def get_oldest(self):
        """Retrieves one element from the queue (with smallest timestamp).

        Blocks if there's no element.
        """
        with self._cv:
            while self._queue_empty():
                self._cv.wait()
            timestamp, kind, value = self._data.pop(0)
            return timestamp, kind, value

    def get_oldest_nowait(self):
        """Retrieves one element from the queue (with smallest timestamp).

        Returns None if the queue is empty.
        """
        with self._cv:
            if not self._data:
                return None
            timestamp, kind, value = self._data.pop(0)
            return timestamp, kind, value

    def qsize(self):
        """Returns approximate size of the queue."""
        with self._cv:
            return len(self._data)

    # Private methods
    def _queue_empty(self):
        """Requires the lock."""
        return len(self._data) == 0

    def _sort_items(self):
        """Requires the lock."""
        self._data.sort()

