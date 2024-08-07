from character import Character
from faction import Faction
from era import Era


class Anthology:
    # TODO: add a docstring
    def __init__(
        self,
        name: str,
        setting: str,
        anthology_type: str,
        factions: list[Faction],
        characters: list[Character],
        year: int = 0,
        era: Era | None = None,
        # TODO: make a history class
        history: str | None = None,
    ) -> None:
        self.name = name
        self.setting = setting
        self.anthology_type = anthology_type
        self.factions = factions
        self.characters = characters
        self._year = year
        self._era = era
        self._history = history

    def __str__(self) -> str:
        return f"Name: {self.name}\nSetting: {self.setting}\nAnthology Type: {self.anthology_type}\nFactions:\n- {"\n- ".join([faction.__str__() for faction in self.factions])}\nCharacters:\n{"\n".join([character.__str__() for character in self.characters])}"

    def __repr__(self) -> str:
        return f"Anthology(name={self.name}, setting={self.setting}, anthology_type={self.anthology_type}, factions={self.factions}, characters={self.characters})"


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
    factions: list[Faction] = []
    while True:
        print(
            "Example factions:\n- Fantasy Races (Elves,Dwarves,Humans,Goblins)\n- Noble Houses/Clans/Kingdoms\n- Corporations"
        )
        faction = input("Enter faction name or enter nothing to end.\n> ")
        if faction == "":
            break
        description = input("Enter faction description:\n> ")
        factions.append(Faction(name=faction, description=description))
    print(
        "Finally, provide at least two characters you want to interact as part of your stories."
    )
    characters: list[Character] = []
    while True:
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
                gender=gender,
                personality=personality,
                faction=faction,
            )
        )

    return Anthology(name, setting, anthology_type, factions, characters)
