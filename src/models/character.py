from __future__ import annotations
from ..utils.llm import OpenAI
from faction import Faction


class Character:
    def __init__(
        self, name: str, age: str, gender: str, personality: str, faction: Faction
    ):
        self.name: str = name
        self.age: int = int(age)
        self.gender: str = gender
        self.personality: str = personality
        self.faction: Faction = faction
        self._conversations: dict[Character | list[Character], OpenAI] = {}
        self._memory: OpenAI = OpenAI()

    def __str__(self) -> str:
        return f"Name: {self.name}\nAge: {self.age}\nGender: {self.gender}\nPersonality: {self.personality}\nFaction: {self.faction}"

    def __repr__(self) -> str:
        return f"Character(name={self.name}, age={self.age}, gender={self.gender}, personality={self.personality}, faction={self.faction})"

    def have_conversation(self, characters: Character | list[Character]) -> None:
        if characters not in self._conversations:
            self._conversations[characters] = OpenAI()
        raise NotImplementedError
