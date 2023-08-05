import threading

from rxbp.acknowledgement.acksubject import AckSubject


class PromiseCounter:
    def __init__(self, value, initial):
        self.lock = threading.RLock()

        self.value = value
        self.counter = initial
        self.promise = AckSubject()

    def acquire(self):
        with self.lock:
            self.counter += 1

    def countdown(self):
        with self.lock:
            self.counter -= 1
            counter = self.counter

        if counter == 0:
            self.promise.on_next(self.value)

