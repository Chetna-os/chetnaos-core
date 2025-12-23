class Limits:
    """
  Hard safety limits.
  """

    def __init__(self, max_autonomy_sec: int = 10, max_tokens: int = 1200):
        self.max_autonomy_sec = max_autonomy_sec
        self.max_tokens = max_tokens

    def check(self, autonomy_sec: int, tokens: int) -> bool:
        if autonomy_sec > self.max_autonomy_sec:
            return False
        if tokens > self.max_tokens:
            return False
        return True
