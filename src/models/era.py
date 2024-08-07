class Era:
    def __init__(self, name: str, duration: int, theme: str) -> None:
        self.name = name
        self.duration = duration
        self.theme = theme
        self._year = 0
        self._events = None
        self._conversations = None
        self._lost_history = None
