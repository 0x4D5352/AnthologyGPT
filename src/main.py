from anthology import Anthology, generate_anthology


def main(interactive: bool = True) -> None:
    if interactive:
        anthology = generate_anthology()
    else:
        anthology = Anthology(
            "Anthology",
            "Fantasy",
            "Endless Desert",
            ["Elves", "Dwarves", "Humans", "Goblins"],
            [
                {
                    "name": "Alice",
                    "age": "25",
                    "gender": "female",
                    "personality": "brave",
                    "faction": "Elves",
                },
                {
                    "name": "Bob",
                    "age": "30",
                    "gender": "male",
                    "personality": "wise",
                    "faction": "Dwarves",
                },
            ],
        )
    print(anthology)


if __name__ == "__main__":
    main(True)
