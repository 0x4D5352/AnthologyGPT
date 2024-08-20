from __future__ import annotations
from random import choice
from entities import Faction, Character
from utils import generate_single_response, generate_summary


class Era:
    """
    A class representing a period of time within an Anthology.

    Attributes:
    Name
    duration
    theme
    factions
    _year
    _summary
    _events

    Methods:
    add_faction()
    remove_faction()
    advance_time()
    generate_possible_events()
    add_event()
    lose_event()
    get_characters()
    have_conversation()
    generate_summary()
    """

    def __init__(
        self,
        name: str,
        duration: int,
        theme: str,
        factions: set[Faction] = set(),
    ) -> None:
        self.name = name
        self.duration = duration
        self.theme = theme
        self.factions = factions
        self._year: int = 0
        self._summary: str = ""
        self._events: list = []

    def add_faction(self, faction: Faction) -> None:
        """
        A simple wrapper around adding factions to the Era
        """
        if faction in self.factions:
            return
        self.factions.add(faction)

    def remove_faction(self, faction: Faction) -> None:
        """
        A simple wrapper around removing factions from the Era
        """
        if faction not in self.factions:
            return
        self.factions.remove(faction)

    def advance_time(self, inc: int = 1) -> int:
        """
        Increment the current year of the Era by some amount and return the number of years advanced. Defaults to 1 year.
        """
        self._year += inc
        if self._year >= self.duration:
            difference = self._year - self.duration
            if difference == 0:
                return difference
            self._year = self.duration
            return inc - difference
        return inc

    def generate_possible_events(self) -> None:
        """
        Use an LLM to generate events that could happen during the current Era that fits with the given theme.
        """
        context = "\n".join([faction.generate_summary() for faction in self.factions])
        prompt = f"""
Come up with a series of 5 to 10 events that could happen in the {self.name} era. The theme of this era is {self.theme}. Here are the following factions, their relationships, and their characters:
{context}
Format your answer as an unordered markdown list like so:
- event a
- event b
- event c
"""
        result = generate_single_response(prompt)
        events = result.split("- ")[1:]
        for event in events:
            event.strip()
            self._events.append(event)

    def add_event(
        self, factions: Faction | list[Faction] | set[Faction], event: str
    ) -> str:
        """
        Add a given event to the history of all factions involved. Return the event in case it needs to be shared elsewhere.
        """
        if isinstance(factions, (list, set)):
            for faction in factions:
                faction._history.add_event(event)
        else:
            factions._history.add_event(event)
        return event

    def lose_event(
        self, factions: Faction | list[Faction] | set[Faction], event: str
    ) -> str:
        if isinstance(factions, (list, set)):
            for faction in factions:
                faction._history.lose_event(event)
        else:
            factions._history.lose_event(event)
        return event

    def get_characters(self, names: set[str] = set()) -> set[Character]:
        """
        Take a set of names and pull the characters from your factions. if no names are given, choose some random characters.
        """
        res: set[Character] = set()
        if len(names) == 0:
            character_count = choice(range(1, 5))
            while len(res) < character_count:
                faction = choice(list(self.factions))
                res.add(faction.get_character())
            return res
        for faction in self.factions:
            for name in names:
                if name not in faction.characters:
                    continue
                res.add(faction.characters[name])
        return res

    def have_conversation(
        self, characters: set[Character], context: str
    ) -> list[dict[str, str]]:
        conversation = []
        participants = {}
        if len(characters) == 1:
            # a monologue!
            active_character = characters.copy().pop()
            participants[active_character] = {
                "others": {active_character},
                "index": active_character.start_conversation({active_character}),
            }
            context = (
                f"You are thinking aloud to yourself about the following:\n{context}"
            )
        else:
            for character in characters:
                others = characters - {character}
                participants[character] = {
                    "others": others,
                    "index": character.start_conversation(others),
                }
            active_character = choice(list(characters))
        last_message = active_character.speak(
            participants[active_character]["others"],
            participants[active_character]["index"],
            context,
        )
        while "</SCENE>" not in last_message["content"]:
            conversation.append(last_message)
            last_message = active_character.speak(
                participants[active_character]["others"],
                participants[active_character]["index"],
            )
            for character in participants[active_character]["others"]:
                character.listen(
                    participants[character]["others"],
                    participants[character]["index"],
                    last_message,
                )
            active_character = choice(list(characters))
        if last_message != conversation[-1]:
            conversation.append(last_message)
        for character in characters:
            character.end_conversation(
                participants[character]["others"],
                participants[character]["index"],
            )
        return conversation

    def generate_summary(self) -> str:
        history = "\n".join(
            [faction._history.generate_summary() for faction in self.factions]
        )
        summary = generate_summary(history)
        # del history
        return summary


class Anthology:
    # TODO: add a docstring
    def __init__(
        self,
        name: str,
        setting: str,
        anthology_type: str,
        year: int = 0,
        eras: dict[str, Era] = {},
    ) -> None:
        self.name = name
        self.setting = setting
        self.anthology_type = anthology_type
        self._year = year
        self._eras = eras
        self._summary = ""

    def generate_summary(self) -> str:
        history = "\n".join([era._summary for era in self._eras.values()])
        summary = generate_summary(history)
        # del history
        return summary

    def create_era(self, name: str, duration: int, theme: str) -> None:
        self._eras[name] = Era(name, duration, theme)

    def add_eras(self, eras: Era | list[Era]) -> None:
        if isinstance(eras, Era):
            self._eras[eras.name] = eras
            return
        for era in eras:
            self.add_eras(era)

    def advance_era(self) -> None:
        return None
