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
        add_to_memories()
        add_to_feelings()
        remember_conversation()
    """

    def __init__(
        self, name: str, age: str, pronouns: str, personality: str, description: str
    ):
        self.name: str = name
        self.age: str = age
        self.pronouns: str = pronouns
        self.personality: str = personality
        self.description: str = description
        self._conversations: dict[Character | set[Character], list[OpenAI]] = {}
        # TODO: get these set up for embeddings. see remember/feel for more docs
        self._memories: OpenAI = OpenAI()
        self._feelings: OpenAI = OpenAI()
        self.__descriptor: str = f"You are {self.name} ({self.pronouns} pronouns). You are a {self.age} year old {self.description}. Your personality is: {self.personality}."

    def __repr__(self) -> str:
        return f"Character(name='{self.name}', age='{self.age}', gender='{self.pronouns}', personality='{self.personality}', description='{self.description}')"

    def start_conversation(self, characters: set[Character]) -> int:
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
        last_character = characters.pop()
        list_of_characters = ", ".join([
            f"{character.name} ({character.pronouns} pronouns)"
            for character in characters
        ])
        list_of_characters += f", and {last_character}"
        del last_character
        memory_of_characters = self.remember(
            f"What do you remember about these people? {list_of_characters}"
        )
        self._conversations[characters][conversation_index].add_message({
            "role": "system",
            "content": f"{self.__descriptor} You're having your {conversation_count} conversation with {list_of_characters}. You know this about them: {memory_of_characters}. Reply in character based on the conversation history and the context provided by the user. Only respond with dialogue, and keep your responses between one word and one paragraph in length. Make sure every participant has had a chance to speak, but if the conversation has gone on long enough, end your message with the string </SCENE>. Prefix all your messages with your name like so: {self.name}: [TEXT]",
        })
        del (
            conversation_count,
            list_of_characters,
            memory_of_characters,
        )
        return conversation_index

    def think(self, context: str) -> str:
        """
        taking in the context as a prompt string, create an ephemeral LLM instance to generate a conclusion about the context - including relevant memories and feelings
        """
        current_thoughts = OpenAI()
        current_thoughts.add_message({
            "role": "system",
            "content": f"{self.__descriptor}. You are about to be given a new piece of information by the user. Think about the information, reflect on your memories and feelings, and come to a conclusion about the information in a way that reflects who you are, describing any justifications, rationale, or emotional response that is appropriate. Respond with a single sentence.",
        })
        relevant_memories = self.remember(context)
        current_thoughts.add_message({
            "role": "user",
            "content": f"memories: {relevant_memories}",
        })
        relevant_feelings = self.feel(context)
        current_thoughts.add_message({
            "role": "user",
            "content": f"feeelings: {relevant_feelings}",
        })
        conclusion = current_thoughts.generate_completion(context)
        del current_thoughts
        return conclusion["content"]

    # TODO: wrap think, feel, and remember in "access_brain" methods

    def remember(self, context: str) -> str:
        """
        This function queries the _memories message history and pulls out information that's important, then returns a prompt completion that gets fed into later calls of the model.
        """
        """
        old docstring:
        This function accesses short and/or long-term memory, slightly modifying long-term memory when accessed.
        thinking of having short term be an LLM chat session that gets removed after conversations, and long-term be embeddings.
        alternately, having short-term and long-term both being embeddings.
        I currently have a few ideas abouw how long term memory could be represented:

        1. add a tiny offset to a token or to clusters of tokens (how much is too much) to represent drift.
        2. execute another LLM call that takes the input, rewords it, and re-embeds it.
        3. i could have a really small long term memory size and constantly summarize and re-embed the information.
        """
        indexer = OpenAI()
        indexer.add_message({
            "role": "system",
            "content": f"{self.__descriptor}. Below is a list of memories that you have. Answer the user's questions based on the memories. If there are no messages between this message and the context, respond with 'nothing'.",
        })
        for message in self._memories._messages:
            indexer.add_message(message)
        response = indexer.generate_completion(
            f"What memories are relevant to the context listed below? Do not quote them directly, only summarize and highlight key points. Limit your response to one short paragraph or less. Context: {context}"
        )
        del indexer
        return response["content"]

    def feel(self, context: str) -> str:
        """
        This function queries the _feelings message history and pulls out information that's important, then returns a prompt completion that gets fed into later calls of the model.
        """
        """
        old docstring:
        NOTE: Not implemented yet.
        This function generates a response simulating the compulsive or instinctual responses.
        The feelings will just be embeddings, but with something weird.
        - maybe the calls have a really high termperature or a really high top_p
        - maybe there's some sum-and-averaging of the embedding
        - i could do some weird mutations
        """
        indexer = OpenAI()
        indexer.add_message({
            "role": "system",
            "content": f"{self.__descriptor}. Below is a list of feelings that you have. Answer the user's questions based on the feelings. If there are no messages between this message and the context, respond with 'nothing'.",
        })
        for message in self._memories._messages:
            indexer.add_message(message)
        response = indexer.generate_completion(
            f"What feelings are relevant to the context listed below? Do not quote them directly, only summarize and highlight key points. Limit your response to one short paragraph or less. Context: {context}"
        )
        del indexer
        return response["content"]

    def speak(
        self,
        characters: set[Character],
        conversation_index: int,
        context: str = "",
    ) -> dict[str, str]:
        """
        generate a completion to add to the current conversation.
        input context, characters, and conversation index.
        output a response from the model as a dict of role and content
        """
        if context:
            thoughts = self.think(context)
            prompt = f"Context: {context}. Your Thoughts: {thoughts}"
            message = self._conversations[characters][
                conversation_index
            ].generate_completion(prompt)
        else:
            message = self._conversations[characters][
                conversation_index
            ].generate_completion()
        return message

    def listen(
        self,
        characters: set[Character],
        conversation_index: int,
        messages: dict[str, str] | list[dict[str, str]],
    ) -> None:
        """
        take in a list of messages (usually responses from other characters) and append then to the current conversation.
        """
        # TODO: test out mutating messages based on the personality of the character
        if not isinstance(messages, list):
            self._conversations[characters][conversation_index].add_message(messages)
            return
        for message in messages:
            self._conversations[characters][conversation_index].add_message(message)

    def add_to_memories(self, conversation: list[dict[str, str]]) -> None:
        summary = OpenAI()
        summary.add_message({
            "role": "system",
            "content": f"{self.__descriptor}. Below is a conversation between two characters, one of whom is you.",
        })
        for message in conversation:
            summary.add_message(message)
        response = summary.generate_completion(
            "Summarize the conversation above. Limit your response to one short paragraph, and only include the most essential information."
        )["content"]
        self._memories.add_message({"role": "user", "content": response})

    def add_to_feelings(self, conversation: list[dict[str, str]]) -> None:
        summary = OpenAI()
        summary.add_message({
            "role": "system",
            "content": f"{self.__descriptor}. Below is a conversation between two characters, one of whom is you.",
        })
        for message in conversation:
            summary.add_message(message)
        response = summary.generate_completion(
            "Summarize your feelings about the conversation above. Use abstract associations, connecting specific people or events with specific emotions. Use single words, avoid complete sentences."
        )["content"]
        self._memories.add_message({"role": "user", "content": response})

    def end_conversation(
        self, characters: set[Character], conversation_index: int
    ) -> None:
        convo = self._conversations[characters][conversation_index]._messages
        self.add_to_memories(convo)
        self.add_to_feelings(convo)
