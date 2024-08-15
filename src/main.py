from anthology import Anthology, Era, Faction
from entities import Character


def have_conversation() -> list[dict[str, str]]:
    prompt = input("What should these characters be talking about?")
    char1 = generate_characters()
    char2 = generate_characters()
    char1_index = char1.start_conversation(char2)
    char2_index = char2.start_conversation(char1)
    last_message = char1.speak(
        char2,
        char1_index,
        prompt,
    )
    convo = []
    convo.append(last_message)
    while True:
        print(last_message["content"])
        if "</SCENE>" in last_message["content"]:
            break
        char2.listen(char1, char2_index, last_message)
        last_message = char2.speak(char1, char2_index)
        convo.append(last_message)
        print(last_message["content"])
        char1.listen(char2, char1_index, last_message)
        last_message = char1.speak(char2, char1_index)
        convo.append(last_message)
    char1.end_conversation(char2, char1_index)
    char2.end_conversation(char1, char2_index)
    print(f"{char1.name} memories:{char1._memories._messages}")
    print(f"{char1.name} feelings:{char1._feelings._messages}")
    print(f"{char2.name} memories:{char2._memories._messages}")
    print(f"{char2.name} feelings:{char2._feelings._messages}")
    return convo


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
    pronouns = input("Character's pronouns:\n> ")
    personality = input("Character's personality:\n> ")
    description = input("Character's description\n> ")
    return Character(
        name=name,
        age=age,
        pronouns=pronouns,
        personality=personality,
        description=description,
    )


def main(interactive: bool = True) -> None:
    ending = have_conversation()
    print("\n".join([message["content"] for message in ending]))


if __name__ == "__main__":
    main(False)
