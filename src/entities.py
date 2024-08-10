from __future__ import annotations
from utils import OpenAI


class Character:
    def __init__(
        self, name: str, age: str, pronouns: str, personality: str, description: str
    ):
        self.name: str = name
        self.age: int = int(age)
        self.pronouns: str = pronouns
        self.personality: str = personality
        self.description: str = description
        self._conversations: dict[Character | set[Character], list[OpenAI]] = {}
        self._memory: OpenAI = OpenAI()
        self._feelings: OpenAI = OpenAI()
        self.__descriptor: str = f"You are {self.name} ({self.pronouns} pronouns). You are a {self.age} year old {self.description}. Your personality is {self.personality}."

    def __str__(self) -> str:
        return f"Name: {self.name}\nAge: {self.age}\nGender: {self.pronouns}\nPersonality: {self.personality}\nDescription: {self.description}"

    def __repr__(self) -> str:
        return f"Character(name={self.name}, age={self.age}, gender={self.pronouns}, personality={self.personality}, description={self.description})"

    def start_conversation(self, characters: Character | set[Character]) -> int:
        """
        Create a new conversation between your character and one or more other characters. To track the conversation, the index is returned for future use.
        """
        if characters not in self._conversations:
            self._conversations[characters] = [OpenAI()]
        else:
            self._conversations[characters].append(OpenAI())
        conversation_index = len(self._conversations[characters]) - 1
        match conversation_index:
            case 0:
                conversation_count = "1st"
            case 1:
                conversation_count = "2nd"
            case 2:
                conversation_count = "3rd"
            case _:
                conversation_count = f"{conversation_index + 1}th"

        if isinstance(characters, set):
            last_character = characters.pop()
            list_of_characters = ", ".join(
                [
                    f"{character.name} ({character.pronouns} pronouns)"
                    for character in characters
                ]
            )
            list_of_characters += f", and {last_character}"
            del last_character
        else:
            list_of_characters = characters.name
        memory_of_characters = "nothing"
        # memory_of_characters = self.remember(f"What do you remember about these people? {list_of_characters}")
        self._conversations[characters][conversation_index].add_message(
            {
                "role": "system",
                "message": f"{self.__descriptor} You're having your {conversation_count} conversation with {list_of_characters}. You know this about them: {memory_of_characters}. Reply in character based on the conversation history and the context provided by the user. If the conversation has gone on long enough, end your message with the string </SCENE>.",
            }
        )
        del (
            conversation_count,
            list_of_characters,
            memory_of_characters,
        )
        return conversation_index

    def think(self, context: str) -> str:
        current_thoughts = OpenAI()
        current_thoughts.add_message(
            {
                "role": "system",
                "message": f"{self.__descriptor}. You are about to be given a new piece of information by the user. Think about the information, reflect on your memories and feelings, and come to a conclusion about the information in a way that reflects how you would really respond.",
            }
        )
        relevant_memories = self.remember(context)
        current_thoughts.add_message({"role": "memories", "message": relevant_memories})
        relevant_feelings = self.feel(context)
        current_thoughts.add_message({"role": "feelings", "message": relevant_feelings})
        conclusion = current_thoughts.generate_completion(context)
        del current_thoughts
        return conclusion["message"]

    def remember(self, context: str) -> str:
        return ""

    def feel(self, context: str) -> str:
        return ""

    def speak(
        self,
        context: str,
        characters: Character | set[Character],
        conversation_index: int,
    ) -> dict[str, str]:
        """
        generate a completion to add to the current conversation.
        input context, characters, and conversation index.
        output a response from the model as a dict of role and content
        """
        # thoughts = self.think(context)
        # prompt = f"Context: {context}. Your Thoughts: {thoughts}"
        prompt = f"Context: {context}."
        message = self._conversations[characters][
            conversation_index
        ].generate_completion(prompt, self.name)
        return message

    def listen(
        self,
        characters: Character | set[Character],
        conversation_index: int,
        messages: list[dict[str, str]],
    ) -> None:
        for message in messages:
            self._conversations[characters][conversation_index].add_message(message)


class Faction:
    def __init__(
        self,
        name: str,
        description: str,
        characters: set[Character] = set(),
    ) -> None:
        self.name = name
        self.description = description
        self.characters = characters
        self._allies = None
        self._enemies = None

    def __str__(self) -> str:
        return f"Name: {self.name}\nDescription: {self.description}"

    def __repr__(self) -> str:
        return f"Faction(name={self.name}, description={self.description})"
