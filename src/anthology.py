from __future__ import annotations
from random import random, choice
from entities import Character
from utils import generate_single_response, generate_summary

LEGEND_CHANCE: float = 0.5


class History:
    """
    A struct for sets of events, with a summary of the remembered history and legends.
    """

    def __init__(self) -> None:
        self._actual_history: set[str] = set()
        self._lost_history: set[str] = set()
        self._remembered_history: set[str] = set()
        self._legends: set[str] = set()
        self._summary: str = ""

    def add_event(self, event: str) -> None:
        self._actual_history.add(event)
        self._remembered_history.add(event)

    def lose_event(self, event: str) -> None:
        self._remembered_history.remove(event)
        self._lost_history.add(event)
        if random() >= LEGEND_CHANCE:
            self.create_legend(event)

    def create_legend(self, event: str) -> None:
        legend = generate_single_response(
            f"Turn the following event into a legend. Mutate aspects of the story to transform it from a real event into some sort of myth or legend. {event}"
        )
        self._legends.add(legend)

    def generate_summary(self) -> str:
        history = "\n".join(self._remembered_history)
        legends = ""
        if len(self._legends) > 0:
            legends = "\n".join(self._legends)
            history += "\n"
        context = history + legends
        summary = generate_summary(context)
        # del history, legends, context
        return summary


class Faction:
    def __init__(
        self,
        name: str,
        description: str,
        characters: dict[str, Character] = {},
    ) -> None:
        self.name = name
        self.description = description
        self.characters = characters
        self._allies: set[Faction] = set()
        self._enemies: set[Faction] = set()
        self._history = History()

    def __str__(self) -> str:
        return f"Name: {self.name}\nDescription: {self.description}"

    def __repr__(self) -> str:
        return f"Faction(name={self.name}, description={self.description})"

    def add_characters(
        self, characters: Character | list[Character] | set[Character]
    ) -> None:
        if isinstance(characters, (list, set)):
            for character in characters:
                self.characters[character.name] = character
            return
        self.characters[characters.name] = characters
        return

    def remove_characters(
        self, characters: Character | list[Character] | set[Character]
    ) -> None:
        if isinstance(characters, (list, set)):
            for character in characters:
                del self.characters[character.name]
            return
        del self.characters[characters.name]
        return

    def get_character(self, name: str = "") -> Character:
        if name == "":
            return choice(list(self.characters.values()))
        res = self.characters[name]
        if not res:
            raise ValueError("character does not exist!")
        return res

    def add_allies(self, allies: Faction | list[Faction] | set[Faction]) -> None:
        if isinstance(allies, (list, set)):
            for ally in allies:
                self._allies.add(ally)
            return
        self._allies.add(allies)
        return

    def remove_allies(self, allies: Faction | list[Faction] | set[Faction]) -> None:
        if isinstance(allies, (list, set)):
            for ally in allies:
                self._allies.remove(ally)
            return
        self._allies.remove(allies)
        return

    def add_enemies(self, enemies: Faction | list[Faction] | set[Faction]) -> None:
        if isinstance(enemies, (list, set)):
            for enemy in enemies:
                self._enemies.add(enemy)
            return
        self._enemies.add(enemies)
        return

    def remove_enemies(self, enemies: Faction | list[Faction] | set[Faction]) -> None:
        if isinstance(enemies, (list, set)):
            for enemy in enemies:
                self._enemies.remove(enemy)
            return
        self._enemies.remove(enemies)
        return

    def generate_summary(self) -> str:
        context = (
            f"Faction Name: {self.name}. Description: {self.description}\nCharacters:"
        )
        characters = "\n".join(
            [character.get_description() for character in self.characters.values()]
        )
        context += "\n" + characters
        # del characters
        if len(self._allies) > 0:
            allies = "\n".join([ally.name for ally in self._allies])
            context += "\n" + allies
            # del allies
        if len(self._enemies) > 0:
            enemies = "\n".join([enemy.name for enemy in self._enemies])
            context += "\n" + enemies
            # del enemies
        return generate_summary(context)


class Era:
    def __init__(
        self,
        name: str,
        duration: int,
        theme: str,
        factions: set[Faction] = set(),
    ) -> None:
        self.name = name
        self.duration = duration
        self.theme = theme
        self.factions = factions
        self._year = 0
        self._summary = ""

    def add_faction(self, faction: Faction) -> None:
        if faction in self.factions:
            return
        self.factions.add(faction)

    def remove_faction(self, faction: Faction) -> None:
        if faction not in self.factions:
            return
        self.factions.remove(faction)

    def _advance_time(self) -> int:
        if self._year >= self.duration:
            return -1
        self._year += 1
        return self._year

    def generate_events(self) -> None:
        context = "\n".join([faction.generate_summary() for faction in self.factions])
        prompt = f"""
Come up with a series of events that could happen in the {self.name} era. The theme of this era is {self.theme}. Here are the following factions, their relationships, and their characters:
{context}
"""
        result = generate_single_response(prompt)

    def add_event(
        self, factions: Faction | list[Faction] | set[Faction], event: str
    ) -> str:
        if isinstance(factions, (list, set)):
            for faction in factions:
                faction._history.add_event(event)
        else:
            factions._history.add_event(event)
        return event

    def lose_event(
        self, factions: Faction | list[Faction] | set[Faction], event: str
    ) -> str:
        if isinstance(factions, (list, set)):
            for faction in factions:
                faction._history.lose_event(event)
        else:
            factions._history.lose_event(event)
        return event

    def get_characters(self, names: set[str] = set()) -> set[Character]:
        """
        Take a set of names and pull the characters from your factions. if no names are given, choose some random characters.
        """
        res: set[Character] = set()
        if len(names) == 0:
            character_count = choice(range(1, 5))
            while len(res) < character_count:
                faction = choice(list(self.factions))
                res.add(faction.get_character())
            return res
        for faction in self.factions:
            for name in names:
                if name not in faction.characters:
                    continue
                res.add(faction.characters[name])
        return res

    def have_conversation(
        self, characters: set[Character], context: str
    ) -> list[dict[str, str]]:
        conversation = []
        participants = {}
        if len(characters) == 1:
            # a monologue! yay
            active_character = characters.copy().pop()
            participants[active_character] = {
                "others": {active_character},
                "index": active_character.start_conversation({active_character}),
            }
            context = (
                f"You are thinking aloud to yourself about the following:\n{context}"
            )
        else:
            for character in characters:
                others = characters - {character}
                participants[character] = {
                    "others": others,
                    "index": character.start_conversation(others),
                }
            active_character = choice(list(characters))
        last_message = active_character.speak(
            participants[active_character]["others"],
            participants[active_character]["index"],
            context,
        )
        while "</SCENE>" not in last_message["content"]:
            conversation.append(last_message)
            last_message = active_character.speak(
                participants[active_character]["others"],
                participants[active_character]["index"],
            )
            for character in participants[active_character]["others"]:
                character.listen(
                    participants[character]["others"],
                    participants[character]["index"],
                    last_message,
                )
            active_character = choice(list(characters))
        if last_message != conversation[-1]:
            conversation.append(last_message)
        for character in characters:
            character.end_conversation(
                participants[character]["others"],
                participants[character]["index"],
            )
        return conversation

    def generate_summary(self) -> str:
        history = "\n".join(
            [faction._history.generate_summary() for faction in self.factions]
        )
        summary = generate_summary(history)
        # del history
        return summary


class Anthology:
    # TODO: add a docstring
    def __init__(
        self,
        name: str,
        setting: str,
        anthology_type: str,
        year: int = 0,
        eras: dict[str, Era] = {},
    ) -> None:
        self.name = name
        self.setting = setting
        self.anthology_type = anthology_type
        self._year = year
        self._eras = eras
        self._summary = ""

    def generate_summary(self) -> str:
        history = "\n".join([era._summary for era in self._eras.values()])
        summary = generate_summary(history)
        # del history
        return summary

    def create_era(self, name: str, duration: int, theme: str) -> None:
        self._eras[name] = Era(name, duration, theme)

    def advance_era(self) -> None:
        return None
