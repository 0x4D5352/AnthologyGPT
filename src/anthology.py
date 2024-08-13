from entities import Faction


class History:
    def __init__(self) -> None:
        self.actual_history = None
        self.lost_history = None
        self.remembered_history = None
        self.legends = None
        self.summary = None


class Era:
    def __init__(
        self,
        name: str,
        duration: int,
        theme: str,
        factions: set[Faction] = set(),
        history: History = History(),
    ) -> None:
        self.name = name
        self.duration = duration
        self.theme = theme
        self.factions = factions
        self.history = history
        self._year = 0
        self._events = None
        self._conversations = None

    def add_faction(self, faction: Faction) -> None:
        if faction in self.factions:
            return
        self.factions.add(faction)

    def remove_faction(self, faction: Faction) -> None:
        if faction not in self.factions:
            return
        self.factions.remove(faction)


class Anthology:
    # TODO: add a docstring
    def __init__(
        self,
        name: str,
        setting: set,
        anthology_type: str,
        year: int = 0,
        era: Era | None = None,
        history: History | None = None,
    ) -> None:
        self.name = name
        self.setting = setting
        self.anthology_type = anthology_type
        self._year = year
        self._era = era
        if history is not None:
            self._history = history
        else:
            self._history = History()
