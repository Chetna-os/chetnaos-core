import time


class HealthChecker:
    """
    System health checks for ChetnaOS runtime.
    """

    def __init__(self):
        self.start_time = time.time()

    def uptime(self):
        return time.time() - self.start_time

    def status(self):
        return {
            "status": "ok",
            "uptime_seconds": round(self.uptime(), 2),
            "timestamp": time.time()
        }


_health_checker = HealthChecker()


def health_check():
    """
    Simple health check function for the API.
    """
    return _health_checker.status()
