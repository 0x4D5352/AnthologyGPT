from __future__ import annotations
from utils import OpenAI


class Character:
    def __init__(
        self, name: str, age: str, pronouns: str, personality: str, faction: Faction
    ):
        self.name: str = name
        self.age: int = int(age)
        self.pronouns: str = pronouns
        self.personality: str = personality
        self.faction: Faction = faction
        self._conversations: dict[Character | set[Character], list[OpenAI]] = {}
        self._memory: OpenAI = OpenAI()

    def __str__(self) -> str:
        return f"Name: {self.name}\nAge: {self.age}\nGender: {self.pronouns}\nPersonality: {self.personality}\nFaction: {self.faction}"

    def __repr__(self) -> str:
        return f"Character(name={self.name}, age={self.age}, gender={self.pronouns}, personality={self.personality}, faction={self.faction})"

    def start_conversation(
        self,
        characters: Character | set[Character],
        previous_messages: list[dict[str, str]],
        current_message: str,
    ) -> None:
        if characters not in self._conversations:
            self._conversations[characters] = [OpenAI()]
        else:
            self._conversations[characters].append(OpenAI())
        if isinstance(characters, set):
            last_character = characters.pop()
            list_of_characters = ", ".join(
                [
                    f"{character.name} ({character.pronouns} pronouns)"
                    for character in characters
                ]
            )
            list_of_characters += f", and {last_character}"
            del last_character
        else:
            list_of_characters = characters.name
        memory_of_characters = "nothing"
        self._conversations[characters][-1].add_message(
            {
                "role": "system",
                "message": f"You are {self.name} ({self.pronouns} pronouns). You are a {self.age} year old {self.faction}. Your personality is {self.personality}. You're having a conversation with {list_of_characters}. You know this about them: {memory_of_characters}. The user is providing you with the most recent message in the conversation, and you are expected to reply in character.",
            }
        )
        if previous_messages:
            for message in previous_messages:
                self._conversations[characters][-1].add_message(message)
        del list_of_characters, memory_of_characters


class History:
    def __init__(self) -> None:
        self.actual_history = None
        self.lost_history = None
        self.remembered_history = None
        self.legends = None
        self.summary = None


class Faction:
    def __init__(
        self,
        name: str,
        description: str,
        characters: set[Character] = set(),
        history: History = History(),
    ) -> None:
        self.name = name
        self.description = description
        self.characters = characters
        self.history = history
        self._allies = None
        self._enemies = None

    def __str__(self) -> str:
        return f"Name: {self.name}\nDescription: {self.description}"

    def __repr__(self) -> str:
        return f"Faction(name={self.name}, description={self.description})"


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
