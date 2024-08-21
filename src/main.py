from anthology import Anthology, Era
from entities import Faction, Character


def generate_setting() -> str:
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
    return ", ".join(res)


def generate_anthology() -> Anthology:
    print(
        "Welcome to Anthology GPT!\nIt's time to create your own Anthology from scratch."
    )
    name: str = input("Enter a name for your Anthology:\n> ")
    print(
        "First, let's set the stage for your Anthology. What kind of setting are you working with?"
    )
    setting: str = generate_setting()
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


def generate_characters(faction: str) -> Character:
    name = input("Character's Name:\n> ")
    age = input("Character's age:\n> ")
    pronouns = input("Character's pronouns:\n> ")
    personality = input("Character's personality:\n> ")
    description = input("Character's description\n> ")
    return Character(
        name=name,
        age=age,
        pronouns=pronouns,
        personality=personality,
        description=description,
        faction=faction,
    )


def main() -> None:
    anthology = generate_anthology()
    print("Anthologies are comprised of Eras; a period of time with a common theme.")
    era = generate_era()
    print("Within each era is a number of factions. You need at least one.")
    add_more = True
    while add_more:
        era.add_faction(generate_faction())
        add_more = (
            False
            if input("add another faction? Y/N (default: N)\n> :") in ["", "N", "n"]
            else True
        )
    print("Within each faction is a number of characters. You need at least two.")
    for faction in era.factions:
        faction.add_characters(generate_characters(faction.name))
        add_more = True
        while add_more:
            faction.add_characters(generate_characters(faction.name))
            add_more = (
                False
                if input("add another character? Y/N (default: N)\n> :")
                in ["", "N", "n"]
                else True
            )
        print(faction.generate_summary())
    anthology.add_eras(era)


if __name__ == "__main__":
    main()
