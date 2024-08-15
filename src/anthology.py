from __future__ import annotations
from random import random
from entities import Character
from utils import OpenAI


class History:
    """
    A struct for sets of events, with a summary of the remembered history and legends.
    """

    def __init__(self) -> None:
        self._actual_history: set[str] = set()
        self._lost_history: set[str] = set()
        self._remembered_history: set[str] = set()
        self._legends: set[str] = set()
        self._summary: str = ""

    def add_event(self, event: str) -> None:
        self._actual_history.add(event)
        self._remembered_history.add(event)

    def lose_event(self, event: str) -> None:
        self._remembered_history.remove(event)
        self._lost_history.add(event)
        if random() >= 0.5:
            self.create_legend(event)

    def create_legend(self, event: str) -> None:
        llm = OpenAI()
        legend = llm.generate_completion(
            f"Turn the following event into a legend. Mutate aspects of the story to move it from a real event to some sort of myth or legend. {event}"
        )["content"]
        del llm
        self._legends.add(legend)

    def generate_sumary(self) -> str:
        llm = OpenAI()
        history = "\n".join(self._remembered_history)
        legends = "\n".join(self._legends)
        summary = llm.generate_completion(
            f"Summarize the following information. Only respond with the summary, keeping your response to the minimum number of words required to create the summary.\n{history}\n{legends}"
        )["content"]
        del llm, history, legends
        return summary


class Faction:
    def __init__(
        self,
        name: str,
        description: str,
        characters: set[Character] = set(),
    ) -> None:
        self.name = name
        self.description = description
        self.characters = characters
        self._allies: set[Faction] = set()
        self._enemies: set[Faction] = set()
        self._history = History()

    def __str__(self) -> str:
        return f"Name: {self.name}\nDescription: {self.description}"

    def __repr__(self) -> str:
        return f"Faction(name={self.name}, description={self.description})"

    def add_characters(
        self, characters: Character | list[Character] | set[Character]
    ) -> None:
        if isinstance(characters, (list, set)):
            for character in characters:
                self.characters.add(character)
            return
        self.characters.add(characters)
        return

    def remove_characters(
        self, characters: Character | list[Character] | set[Character]
    ) -> None:
        if isinstance(characters, (list, set)):
            for character in characters:
                self.characters.remove(character)
            return
        self.characters.remove(characters)
        return

    def add_allies(self, allies: Faction | list[Faction] | set[Faction]) -> None:
        if isinstance(allies, (list, set)):
            for ally in allies:
                self._allies.add(ally)
            return
        self._allies.add(allies)
        return

    def remove_allies(self, allies: Faction | list[Faction] | set[Faction]) -> None:
        if isinstance(allies, (list, set)):
            for ally in allies:
                self._allies.remove(ally)
            return
        self._allies.remove(allies)
        return

    def add_enemies(self, enemies: Faction | list[Faction] | set[Faction]) -> None:
        if isinstance(enemies, (list, set)):
            for enemy in enemies:
                self._enemies.add(enemy)
            return
        self._enemies.add(enemies)
        return

    def remove_enemies(self, enemies: Faction | list[Faction] | set[Faction]) -> None:
        if isinstance(enemies, (list, set)):
            for enemy in enemies:
                self._enemies.remove(enemy)
            return
        self._enemies.remove(enemies)
        return


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

    def add_faction(self, faction: Faction) -> None:
        if faction in self.factions:
            return
        self.factions.add(faction)

    def remove_faction(self, faction: Faction) -> None:
        if faction not in self.factions:
            return
        self.factions.remove(faction)

    def advance_time(self) -> int:
        if self._year >= self.duration:
            self._year = self.duration
        else:
            self._year += 1
        return self._year


class Anthology:
    # TODO: add a docstring
    def __init__(
        self,
        name: str,
        setting: set,
        anthology_type: str,
        year: int = 0,
        era: Era | None = None,
        history: History = History(),
    ) -> None:
        self.name = name
        self.setting = setting
        self.anthology_type = anthology_type
        self._year = year
        self._era = era
        self._history = history
