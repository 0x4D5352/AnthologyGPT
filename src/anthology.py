from __future__ import annotations
from utils import OpenAI


class History:
    def __init__(self) -> None:
        self.actual_history = None
        self.lost_history = None
        self.remembered_history = None
        self.legends = None
        self.summary = None


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
        self._feelings: OpenAI = OpenAI()
        self.__descriptor: str = f"You are {self.name} ({self.pronouns} pronouns). You are a {self.age} year old {self.faction}. Your personality is {self.personality}."

    def __str__(self) -> str:
        return f"Name: {self.name}\nAge: {self.age}\nGender: {self.pronouns}\nPersonality: {self.personality}\nFaction: {self.faction}"

    def __repr__(self) -> str:
        return f"Character(name={self.name}, age={self.age}, gender={self.pronouns}, personality={self.personality}, faction={self.faction})"

    def start_conversation(self, characters: Character | set[Character]) -> int:
        """
        Create a new conversation between your character and one or more other characters. To track the conversation, the index is returned for future use.
        """
        if characters not in self._conversations:
            self._conversations[characters] = [OpenAI()]
        else:
            self._conversations[characters].append(OpenAI())
        conversation_index = len(self._conversations[characters]) - 1
        match conversation_index:
            case 0:
                conversation_count = "1st"
            case 1:
                conversation_count = "2nd"
            case 2:
                conversation_count = "3rd"
            case _:
                conversation_count = f"{conversation_index + 1}th"

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
        self._conversations[characters][conversation_index].add_message(
            {
                "role": "system",
                "message": f"{self.__descriptor} You're having your {conversation_count} conversation with {list_of_characters}. You know this about them: {memory_of_characters}. The user is providing you withe most recent message in the conversation, and you are expected to reply in character.",
            }
        )
        del (
            conversation_count,
            list_of_characters,
            memory_of_characters,
        )
        return conversation_index

    def think(self, context: str) -> str:
        current_thought = OpenAI()
        current_thought.add_message(
            {
                "role": "system",
                "message": f"{self.__descriptor}. You are about to be given a new piece of information by the user. Think about the information, reflect on your memories and feelings, and come to a conclusion about the information in a way that reflects how you would really respond.",
            }
        )
        relevant_memories = self.remember(context)
        current_thought.add_message({"role": "memories", "message": relevant_memories})
        return ""

    def remember(self, context: str | Character | OpenAI) -> str:
        return ""

    def feel(self, context: str) -> str:
        return ""

    def speak(self, characters: Character | set[Character]) -> dict[str, str]:
        return {}

    def listen(
        self,
        characters: Character | set[Character],
        conversation_index: int,
        message: dict[str, str],
    ) -> None:
        self._conversations[characters][conversation_index].add_message(message)


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
