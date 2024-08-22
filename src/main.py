from dotenv import load_dotenv
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


def main(interactive: bool = True) -> None:
    if interactive:
        anthology = generate_anthology()
        print(
            "Anthologies are comprised of Eras; a period of time with a common theme."
        )
        era = generate_era()
        print("Within each era is a number of factions. You need at least one.")
        add_more = True
        while add_more:
            era.add_faction(generate_faction())
            add_more = (
                False
                if input("add another faction? Y/N (default: N)\n> ") in ["", "N", "n"]
                else True
            )
        print("Within each faction is a number of characters. You need at least two.")
        for faction in era.factions.values():
            faction.add_characters(generate_characters(faction.name))
            add_more = True
            while add_more:
                faction.add_characters(generate_characters(faction.name))
                add_more = (
                    False
                    if input("add another character? Y/N (default: N)\n> ")
                    in ["", "N", "n"]
                    else True
                )
            print(faction.generate_summary())
    else:
        anthology = Anthology("The Island", "Fantasy", "Island Nation")
        era = Era("First", 1, "Betrayal")
        north = Faction(
            "North Islanders", "A stocky tribal group that live in the high mountains."
        )
        jarric = Character(
            "Jarric Cloakstorm",
            "45",
            "He/Him",
            "A cold and calculating leader with a fierce loyalty to his tribe and a caring demeanor underneath.",
            "Tall, with long brown hair and blue eyes. He has multiple scars across his face.",
            north.name,
        )
        wyndham = Character(
            "Wyndham Cloakstorm",
            "20",
            "He/Him",
            "A friendly and naive heir to the throne, untainted by the corruption of the world.",
            "Tall, with long brown hair and blue eyes.",
            north.name,
        )
        north.add_characters([jarric, wyndham])
        era.add_faction(north)
        south = Faction(
            "South Islanders",
            "A democratic group that inhabits the tropical coastline.",
        )
        moreen = Character(
            "Moreen D'Archon",
            "37",
            "She/Her",
            "A proud and noble Premier who would do anything to protect her people.",
            "Short, dark-skinned, with curly brown hair and dark grey eyes.",
            south.name,
        )
        folstik = Character(
            "Folstik Dorner",
            "31",
            "He/Him",
            "A wise scholar with poor social skills, who wishes to help whenever he can but often acts too cold for his own good.",
            "Tall, lanky and red-haired with large spectacles and a disheveled-but-not-dirty appearance.",
            south.name,
        )
        south.add_characters([moreen, folstik])
        era.add_faction(south)
    anthology.add_eras(era)
    anthology.advance_era(era.name)
    print(anthology._summary)


if __name__ == "__main__":
    load_dotenv()
    main()
