class Anthology:
    def __init__(
        self,
        name: str,
        setting: str,
        anthology_type: str,
        factions: list[str],
        characters: list[dict[str, str]],
    ) -> None:
        self.name = name
        self.setting = setting
        self.anthology_type = anthology_type
        self.factions = factions
        self.characters = characters
        self.year = 0

    def __str__(self) -> str:
        return f"Name: {self.name}\nSetting: {self.setting}\nAnthology Type: {self.anthology_type}\nFactions: {self.factions}\nCharacters: {self.characters}"


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
        "Now, let's design your Anthology's theme. What type of Anthology will your characters inhabit?"
    )
    anthology_type: str = input(
        "Example Anthologys:\n- Endless Desert/Ocean\n- Endless Metropolis\n- Earth-like\n> "
    )
    print(
        "Next, identify at least two factions you want to be involved in your Anthology."
    )
    factions: list[str] = []
    while True:
        print(
            "Example factions:\n- Fantasy Races (Elves,Dwarves,Humans,Goblins)\n- Noble Houses/Clans/Kingdoms\n- Corporations"
        )
        faction = input("Enter faction name or enter nothing to end.\n> ")
        if faction == "":
            break
        factions.append(faction)
    print(
        "Finally, provide at least two characters you want to interact as part of your stories."
    )
    characters: list[dict[str, str]] = []
    while True:
        character: dict[str, str] = {}
        print("Enter character name or enter nothing to end.")
        character["name"] = input("Character's Name:\n> ")
        if character["name"] == "":
            break
        character["age"] = input("Character's age:\n> ")
        character["gender"] = input("Character's gender:\n> ")
        character["personality"] = input("Character's personality:\n> ")
        character["faction"] = input("Character's faction\n> ")
        characters.append(character)

    return Anthology(name, setting, anthology_type, factions, characters)
