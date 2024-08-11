from __future__ import annotations
from utils import OpenAI


class Character:
    """
    A class representing a character in the Anthology.

    Attributes:
        name
        age
        pronouns
        personality
        description

    Methods:
        start_conversation()
        think()
        remember()
        feel()
        speak()
        listen()
    """

    def __init__(
        self, name: str, age: str, pronouns: str, personality: str, description: str
    ):
        self.name: str = name
        self.age: int = int(age)
        self.pronouns: str = pronouns
        self.personality: str = personality
        self.description: str = description
        self._conversations: dict[Character | set[Character], list[OpenAI]] = {}
        # TODO: get these set up for embeddings. see remember/feel for more docs
        self._memory: list[dict[str, str | int | list[float]]] | OpenAI = OpenAI()
        self._feelings: list[dict[str, str | int | list[float]]] | OpenAI = OpenAI()
        self.__descriptor: str = f"You are {self.name} ({self.pronouns} pronouns). You are a {self.age} year old {self.description}. Your personality is {self.personality}."

    def __repr__(self) -> str:
        return f"Character(name='{self.name}', age='{self.age}', gender='{self.pronouns}', personality='{self.personality}', description='{self.description}')"

    def start_conversation(self, characters: Character | set[Character]) -> int:
        """
        Create a new conversation between your character and one or more other characters. To track the conversation, the index is returned for future use.
        """
        if characters not in self._conversations:
            self._conversations[characters] = [OpenAI()]
        else:
            self._conversations[characters].append(OpenAI())
        conversation_index = len(self._conversations[characters])
        match conversation_index:
            case 0:
                raise ValueError("empty index!")
            case 1:
                conversation_count = "1st"
            case 2:
                conversation_count = "2nd"
            case 3:
                conversation_count = "3rd"
            case _:
                conversation_count = f"{conversation_index + 1}th"

        conversation_index -= 1  # for indexing/OBO avoidance
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
                "content": f"{self.__descriptor} You're having your {conversation_count} conversation with {list_of_characters}. You know this about them: {memory_of_characters}. Reply in character based on the conversation history and the context provided by the user. If the conversation has gone on long enough, end your message with the string </SCENE>.",
            }
        )
        del (
            conversation_count,
            list_of_characters,
            memory_of_characters,
        )
        return conversation_index

    def think(self, context: str) -> str:
        """
        NOTE: memories and feelings are not implemented yet
        taking in the context as a prompt string, create an ephemeral LLM instance to generate a conclusion about the context - including relevant memories and feelings
        """
        current_thoughts = OpenAI()
        current_thoughts.add_message(
            {
                "role": "system",
                "content": f"{self.__descriptor}. You are about to be given a new piece of information by the user. Think about the information, reflect on your memories and feelings, and come to a conclusion about the information in a way that reflects how you would really respond.",
            }
        )
        # relevant_memories = self.remember(context)
        # current_thoughts.add_message({"role": "memories", "content": relevant_memories})
        current_thoughts.add_message(
            {"role": "system", "content": "memories: you are up for anything"}
        )
        # relevant_feelings = self.feel(context)
        # current_thoughts.add_message({"role": "feelings", "content": relevant_feelings})
        current_thoughts.add_message(
            {"role": "system", "content": "feelings: you feel pretty happy"}
        )
        conclusion = current_thoughts.generate_completion(context)
        del current_thoughts
        return conclusion["content"]

    def remember(self, context: str) -> str:
        """
        NOTE: Not implemented yet.
        This function accesses short and/or long-term memory, slightly modifying long-term memory when accessed.
        thinking of having short term be an LLM chat session that gets removed after conversations, and long-term be embeddings.
        alternately, having short-term and long-term both being embeddings.
        I currently have a few ideas abouw how long term memory could be represented:

        1. add a tiny offset to a token or to clusters of tokens (how much is too much) to represent drift.
        2. execute another LLM call that takes the input, rewords it, and re-embeds it.
        3. i could have a really small long term memory size and constantly summarize and re-embed the information.
        """
        raise NotImplementedError

    def feel(self, context: str) -> str:
        """
        NOTE: Not implemented yet.
        This function generates a response simulating the compulsive or instinctual responses.
        The feelings will just be embeddings, but with something weird.
        - maybe the calls have a really high termperature or a really high top_p
        - maybe there's some sum-and-averaging of the embedding
        - i could do some weird mutations
        """
        raise NotImplementedError

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
        ].generate_completion(prompt)
        return message

    def listen(
        self,
        characters: Character | set[Character],
        conversation_index: int,
        messages: list[dict[str, str]],
    ) -> None:
        """
        take in a list of messages (usually responses from other characters) and append then to the current conversation.
        """
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
