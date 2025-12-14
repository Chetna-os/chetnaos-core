import time


class Metrics:
    """
    Simple in-memory metrics tracker.
    """

    def __init__(self):
        self.counters = {}
        self.timings = {}

    def increment(self, name: str, value: int = 1):
        self.counters[name] = self.counters.get(name, 0) + value

    def record_time(self, name: str, duration: float):
        self.timings.setdefault(name, []).append(duration)

    def snapshot(self):
        return {
            "counters": dict(self.counters),
            "timings": {
                k: {
                    "count": len(v),
                    "avg": sum(v) / len(v) if v else 0
                }
                for k, v in self.timings.items()
            }
        }


_metrics = Metrics()


def record_metric(name: str, value: float):
    """
    Record a timing metric.
    """
    _metrics.record_time(name, value)
