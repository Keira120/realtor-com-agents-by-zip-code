import threading
import time

class RateLimiter:
    """
    Simple rate limiter that enforces a maximum number of calls per minute.

    This implementation is process-local and thread-safe enough for a small
    scraper running on a single machine.
    """

    def __init__(self, calls_per_minute: int) -> None:
        if calls_per_minute <= 0:
            raise ValueError("calls_per_minute must be positive.")
        self.interval = 60.0 / float(calls_per_minute)
        self._lock = threading.Lock()
        self._last_call = 0.0

    def wait(self) -> None:
        with self._lock:
            now = time.time()
            elapsed = now - self._last_call
            if elapsed < self.interval:
                time.sleep(self.interval - elapsed)
            self._last_call = time.time()