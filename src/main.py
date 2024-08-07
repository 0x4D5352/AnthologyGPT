from anthology import Anthology, generate_anthology
from character import Character
from faction import Faction


def main(interactive: bool = True) -> None:
    if interactive:
        anthology = generate_anthology()
    else:
        anthology = Anthology(
            "Anthology",
            "Fantasy",
            "Endless Desert",
            [
                Faction("Elves", "A wise and ancient race of tall, slender humanoids."),
                Faction("Dwarves", "A short and sturdy race of miners and craftsmen."),
                Faction("Humans", "The most common and adaptable of all the races."),
                Faction("Goblins", "A mischievous and cunning race of scavengers."),
            ],
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
        )
    print(anthology)


if __name__ == "__main__":
    main(False)
