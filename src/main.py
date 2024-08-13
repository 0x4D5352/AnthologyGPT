from anthology import Anthology, Era
from entities import Faction, Character

# TODO: add a "remember conversation" or "add memory" method to the characters


def have_conversation() -> dict[str, str]:
    char1 = generate_characters()
    char2 = generate_characters()
    char1_index = char1.start_conversation(char2)
    char2_index = char2.start_conversation(char1)
    last_message = char1.speak(
        char2,
        char1_index,
        f"You just found out {char2.name} is having their birthday tomorrow!",
    )
    while True:
        if "</SCENE>" in last_message["content"]:
            break
        print(last_message["content"])
        char2.listen(char1, char2_index, last_message)
        last_message = char2.speak(char1, char2_index)
        print(last_message["content"])
        char1.listen(char2, char1_index, last_message)
        last_message = char1.speak(char2, char1_index)
    return last_message


def generate_setting() -> set:
    res = set()
    while True:
        print(
            "Enter a theme or genre to describe your setting, or enter nothing to stop."
        )
        setting: str = input(
            "Example settings:\n- Fantasy\n- Victorian\n- Cyberpunk\n- Science Fiction\n> "
        )
        if setting == "":
            break
        res.add(setting)
        print(f"current setting: {", ".join(res)}")
    if len(res) == 0:
        raise ValueError("You need at least one setting!")
    return res


def generate_anthology() -> Anthology:
    print(
        "Welcome to Anthology GPT!\nIt's time to create your own Anthology from scratch."
    )
    name: str = input("Enter a name for your Anthology:\n> ")
    print(
        "First, let's set the stage for your Anthology. What kind of setting are you working with?"
    )
    setting: set = generate_setting()
    print(
        "Now, let's design your Anthology's \"world\". What type of Anthology will your characters inhabit?"
    )
    anthology_type: str = input(
        "Example types:\n- Endless Desert/Ocean\n- Endless Metropolis\n- Earth-like\n> "
    )
    return Anthology(name, setting, anthology_type)


def generate_era() -> Era:
    name: str = input("Enter a name for your Era:\n> ")
    duration: str = input("Enter a duration for your Era:\n> ")
    theme: str = input("Enter a theme for your Era:\n> ")
    return Era(name, int(duration), theme)


def generate_faction() -> Faction:
    print(
        "Example factions:\n- Fantasy Races (Elves,Dwarves,Humans,Goblins)\n- Noble Houses/Clans/Kingdoms\n- Corporations"
    )
    faction = input("Enter faction name.\n> ")
    description = input("Enter faction description:\n> ")
    return Faction(name=faction, description=description)


def generate_characters() -> Character:
    name = input("Character's Name:\n> ")
    age = input("Character's age:\n> ")
    gender = input("Character's gender:\n> ")
    personality = input("Character's personality:\n> ")
    description = input("Character's description\n> ")
    return Character(
        name=name,
        age=age,
        pronouns=gender,
        personality=personality,
        description=description,
    )


def main(interactive: bool = True) -> None:
    if interactive:
        anthology = generate_anthology()
    else:
        anthology = Anthology(
            "Anthology",
            {"Fantasy"},
            "Endless Desert",
        )
    print(anthology)
    ending = have_conversation()
    print(ending["content"])


if __name__ == "__main__":
    main(False)
