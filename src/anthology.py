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

    def start_conversation(self, characters: Character | set[Character]) -> None:
        if characters not in self._conversations:
            self._conversations[characters] = [OpenAI()]
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
            self._conversations[characters][0].add_message(
                {
                    "role": "system",
                    "message": f"You are {self.name} ({self.pronouns} pronouns). You are a {self.age} year old {self.faction}. Your personality is {self.personality}. You're having a conversation with {list_of_characters}. You know this about them: {memory_of_characters}. The user is providing you withe most recent message in the conversation, and you are expected to reply in character.",
                }
            )
            del list_of_characters, memory_of_characters
        else:
            self._conversations[characters].append(OpenAI())
            conversation_number = len(self._conversations[characters])


class Faction:
    def __init__(self, name: str, description: str, characters: set[Character]) -> None:
        self.name = name
        self.description = description
        self.characters = characters
        self._allies = None
        self._enemies = None

    def __str__(self) -> str:
        return f"Name: {self.name}\nDescription: {self.description}"

    def __repr__(self) -> str:
        return f"Faction(name={self.name}, description={self.description})"


class Era:
    def __init__(
        self, name: str, duration: int, theme: str, factions: set[Faction]
    ) -> None:
        self.name = name
        self.duration = duration
        self.theme = theme
        self.factions = factions
        self._year = 0
        self._events = None
        self._conversations = None
        self._lost_history = None

    def add_faction(self, faction: Faction) -> None:
        if faction in self.factions:
            return
        self.factions.add(faction)

    def remove_faction(self, name: str) -> None:
        if name not in [faction.name for faction in self.factions]:
            return
        target = None
        for faction in self.factions:
            if faction.name == name:
                target = faction
        if target is not None:
            self.factions.remove(target)


class History:
    def __init__(self) -> None:
        self.actual_history = None
        self.remembered_history = None
        self.legends = None
        self.summary = None


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


def generate_anthology() -> Anthology:
    print(
        "Welcome to Anthology GPT!\nIt's time to create your own Anthology from scratch."
    )
    name: str = input("Enter a name for your Anthology:\n> ")
    print(
        "First, let's set the stage for your Anthology. What kind of setting are you working with?"
    )
    setting: str = input(
        "Example settings:\n- Fantasy\n- Victorian\n- Cyberpunk\n- Science Fiction\n> "
    )
    print(
        "Now, let's design your Anthology's \"world\". What type of Anthology will your characters inhabit?"
    )
    anthology_type: str = input(
        "Example types:\n- Endless Desert/Ocean\n- Endless Metropolis\n- Earth-like\n> "
    )
    print(
        "Next, identify at least two factions you want to be involved in your Anthology."
    )
    factions: set[Faction] = set()
    while True:
        print(
            "Example factions:\n- Fantasy Races (Elves,Dwarves,Humans,Goblins)\n- Noble Houses/Clans/Kingdoms\n- Corporations"
        )
        faction = input("Enter faction name or enter nothing to end.\n> ")
        if faction == "":
            break
        description = input("Enter faction description:\n> ")
        factions.add(Faction(name=faction, description=description))
    print(
        "Finally, provide at least two characters you want to interact as part of your stories."
    )
    characters: list[Character] = []
    still_generating_characters: bool = True
    while still_generating_characters:
        print("Enter character name or enter nothing to end.")
        name = input("Character's Name:\n> ")
        if name == "":
            break
        age = input("Character's age:\n> ")
        gender = input("Character's gender:\n> ")
        personality = input("Character's personality:\n> ")
        faction = input("Character's faction\n> ")
        characters.append(
            Character(
                name=name,
                age=age,
                pronouns=gender,
                personality=personality,
                faction=faction,
            )
        )

    return Anthology(name, setting, anthology_type, factions, characters)
