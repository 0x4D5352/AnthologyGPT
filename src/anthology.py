from __future__ import annotations
from random import choice
from entities import Faction, Character
from utils import generate_single_response, generate_summary, save_json, save_summary


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
        factions: dict[str, Faction] = {},
    ) -> None:
        self.name = name
        self.duration = duration
        self.theme = theme
        self.factions = factions
        self._year: int = 0
        self._summary: str = ""
        self._events: list[str] = []

    def add_faction(self, faction: Faction) -> None:
        """
        A simple wrapper around adding factions to the Era
        """
        self.factions[faction.name] = faction
        # save_json(f"{self.name}_factions", self.factions)

    def remove_faction(self, faction: Faction) -> None:
        """
        A simple wrapper around removing factions from the Era
        """
        del self.factions[faction.name]
        # save_json(f"{self.name}_factions", self.factions)

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
        context = "\n".join([
            faction.generate_summary() for faction in self.factions.values()
        ])
        prompt = f"""
Come up with a series of 5 to 10 events that could happen in the {self.name} era. The theme of this era is {self.theme}. Here are the following factions, their relationships, and their characters:
{context}
Format your answer as an unordered markdown list like so:
- event a
- event b
- event c
"""
        result = generate_single_response(prompt)
        print(f"events: {result}\n")
        events = result.split("- ")[1:]
        for event in events:
            event.strip()
            self._events.append(event)
        save_json(f"{self.name}_events", self._events)

    def get_next_event(self) -> str:
        next = self._events.pop()
        save_json(f"{self.name}_events", self._events)
        return next

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
                faction = choice(list(self.factions.values()))
                res.add(faction.get_character())
            return res
        for faction in self.factions.values():
            for name in names:
                if name not in faction.characters:
                    continue
                res.add(faction.characters[name])
        return res

    def have_conversation(
        self, characters: set[Character], context: str
    ) -> list[dict[str, str]]:
        """
        Generate a conversation between some set of characters, returning the resulting conversation.
        """
        print(
            f"starting a convo with {" ".join([character.name for character in characters])}"
        )
        conversation: list[dict[str, str]] = []
        participants = {}
        if len(characters) == 1:
            # a monologue!
            active_character = characters.copy().pop()
            others = frozenset(characters)
            participants[active_character] = {
                "others": others,
                "index": active_character.start_conversation(others),
            }
            context = (
                f"You are thinking aloud to yourself about the following:\n{context}"
            )
        else:
            for character in characters:
                others = frozenset(characters - {character})
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
        conversation.append(last_message)
        while "</SCENE>" not in last_message["content"]:
            for character in participants[active_character]["others"]:
                character.listen(
                    participants[character]["others"],
                    participants[character]["index"],
                    last_message,
                )
            active_character = choice(list(characters))
            last_message = active_character.speak(
                participants[active_character]["others"],
                participants[active_character]["index"],
            )
            conversation.append(last_message)
            convo = "\n".join([
                message["content"] for message in conversation if len(conversation) > 0
            ])
            print(f"{convo}\n")

        convo = "\n".join([
            message["content"] for message in conversation if len(conversation) > 0
        ])
        print(f"{convo}\n")
        try:
            if last_message != conversation[-1]:
                conversation.append(last_message)
                for character in participants[active_character]["others"]:
                    character.listen(
                        participants[character]["others"],
                        participants[character]["index"],
                        last_message,
                    )
        except IndexError as e:
            print("something's happening with this convo...")
            print(e)
        for character in characters:
            character.end_conversation(
                participants[character]["others"],
                participants[character]["index"],
            )
        return conversation

    def generate_summary(self) -> str:
        history = "\n".join([
            faction._history.generate_summary() for faction in self.factions.values()
        ])
        summary = generate_summary(history)
        # del history
        print(summary)
        save_summary(f"{self.name}_summary", summary)
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
        print(f"anthology summary: {summary}")
        save_summary(f"{self.name}_summary", summary)
        return summary

    def create_era(self, name: str, duration: int, theme: str) -> None:
        self._eras[name] = Era(name, duration, theme)

    def add_eras(self, eras: Era | list[Era]) -> None:
        if isinstance(eras, Era):
            self._eras[eras.name] = eras
        else:
            for era in eras:
                self.add_eras(era)
        # save_json(f"{self.name}_eras", self._eras)

    def advance_era(self, era: str) -> None:
        starting_year = self._year
        current_era = self._eras[era]
        while self._year <= starting_year + current_era.duration:
            self._year += current_era.advance_time()
            current_era.generate_possible_events()
            while len(current_era._events) > 0:
                next_event = current_era.get_next_event()
                characters = current_era.get_characters()
                current_era.have_conversation(characters, next_event)
                for character in characters:
                    event = character.think(
                        "You are telling your faction about the most recent conversation you had. Generate a third person summary that your faction would add to their history. Keep the summary between one and three sentences. Only include the summary in your response."
                    )
                    current_era.factions[character.faction]._history.add_event(event)
                    for other_character in current_era.factions[
                        character.faction
                    ].characters:
                        if other_character is character:
                            continue
                        character.add_to_memories([{"role": "user", "content": event}])
            for faction in current_era.factions.values():
                lost_count = (
                    choice(range(len(faction._history._remembered_history))) // 4 + 1
                )
                for _ in range(lost_count):
                    lost_event = choice(list(faction._history._remembered_history))
                    faction._history.lose_event(lost_event)
                    for character in faction.characters.values():
                        for index, memory in enumerate(character._memories._messages):
                            if lost_event == memory["content"]:
                                # TODO: make a lose memory method
                                del character._memories._messages[index]
        self._summary = self.generate_summary()
