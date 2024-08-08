from anthology import Anthology, Era, Faction, Character


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
    print(
        "Next, identify at least two factions you want to be involved in your Anthology."
    )
    return Anthology(name, setting, anthology_type)


def generate_era():
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


if __name__ == "__main__":
    main(False)


"""

            {
                Faction("Elves", "A wise and ancient race of tall, slender humanoids."),
                Faction("Dwarves", "A short and sturdy race of miners and craftsmen."),
                Faction("Humans", "The most common and adaptable of all the races."),
                Faction("Goblins", "A mischievous and cunning race of scavengers."),
            },
            [
                Character(
                    name="Alice",
                    age="25",
                    gender="female",
                    personality="brave",
                    faction="Elves",
                ),
                Character(
                    name="Bob",
                    age="30",
                    gender="male",
                    personality="wise",
                    faction="Dwarves",
                ),
            ],
    """
