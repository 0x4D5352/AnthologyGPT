from dotenv import load_dotenv
import requests
from env import OPENAI_API_KEY

# OPENAI_API_KEY = load_dotenv()
EXAMPLE_OPENAI_COMPLETION_REQUEST_BODY = {
    "model": "foo-345",
    "temperature": 1,
    "top_p": 1,  # NOTE: Only change temperate OR top_p, not both!
    "messages": [
        {"role": "system", "content": "foo"},
        {"role": "user", "content": "foobar"},
    ],
    "stream": False,  # NOTE: Should never be True, but if using Ollama you must explicity set False
}

OPENAI_RESPONSE_SCHEMA = {
    "id": "foo",
    "object": "foobar",
    "created": 0,
    "model": "foo-345",
    "system_fingerprint": "foo_12304",
    "choices": [
        {
            "index": 0,
            "message": {"role": "assistant", "content": "foo"},
            "logprobs": None,
            "finish_reason": "stop",
        }
    ],
    "usage": {"prompt_tokens": 9, "completion_tokens": 12, "total_tokens": 21},
}


class LLM:
    """
    A wrapper for a chain of interactions with a Large Language Model.

    Attributes:
        source
        endpoint
        headers
        _messages
        settings

    Methods:
        generate_completion()
        generate_embeddings()
        add_message()
        adjust_settings()
    """

    def __init__(
        self,
        source: str,
        endpoint: str,
        headers: dict[str, str],
    ) -> None:
        self.source: str = source
        self.endpoint: str = endpoint
        self.headers: dict[str, str] = headers
        self._messages: list[dict[str, str]] = []
        self._settings: dict[str, str | int | float | bool] = {
            "model": "null",
            "temperature": 1,
            "top_p": 1,
            "stream": False,
        }
        # self._session: requests.Session = requests.Session()

    def __repr__(self) -> str:
        return f"LLM(source='{self.source}', endpoint='{self.endpoint}', headers={self.headers})"

    def generate_completion(self, prompt: str):
        raise NotImplementedError

    def generate_embeddings(self, input: str):
        raise NotImplementedError

    def add_message(self, message: dict[str, str]) -> None:
        """takes a dict ({"role": "system/user/assistant", "content": "message contents"}) and appends it to self._messages,"""
        self._messages.append(message)

    def adjust_setting(self, key: str, value: str | int | float | bool) -> None:
        """
        takes a key/value pair and updates the relevant setting for the LLM. won't allow changes to both temp AND top_p.
        """
        if (key == "temperature" and self._settings["top_p"] != 1) or (
            key == "top_p" and self._settings["temperature"] != 1
        ):
            raise ValueError("do not adjust both temperature and top_p!")
        self._settings[key] = value


class OpenAI(LLM):
    """
    A class representing a chain of interactions with OpenAI's LLM, ChatGPT

    Attributes:
        source: a short name to identify where the LLM is coming from
        endpoint: the primary URL pointing towards the server that we send requests to.
        headers: Key/Value pairs that get passed in the reque
        _messages: a list holding the interactions with this instance of the model.
        _settings: Key/Value pairs with the configuration options passed to the model.

    Methods:
        generate_completion(): Give a prompt (and optionally, a role) and get a response, saving both to the message history.
        generate_embedding(): Give a string of text, a list of strings, a list of tokens (int), or a list of lists of tokens and get an embedding list in response.
    """

    def __init__(self):
        headers = {
            "Authorization": f"Bearer {OPENAI_API_KEY}",
            "Content-Type": "application/json",
        }
        super().__init__(
            source="OpenAI", endpoint="https://api.openai.com/v1/", headers=headers
        )
        self._settings["model"] = "gpt-4o"
        del headers

    def generate_completion(self, prompt: str = "") -> dict[str, str]:
        """
        generate a chat completion response based on the prompt and the existing chat history for the model.
        """
        endpoint = self.endpoint + "chat/completions"
        request = EXAMPLE_OPENAI_COMPLETION_REQUEST_BODY.copy()
        for setting in self._settings.keys():
            request[setting] = self._settings[setting]
        if prompt:
            message = {"role": "user", "content": prompt}
            self.add_message(message)
        request["messages"] = self._messages
        response = requests.post(
            url=endpoint, json=request, headers=self.headers
        ).json()
        # TODO: handle the case of a JSON error
        response_message = response["choices"][0]["message"]
        if response_message["refusal"] is not None:
            raise ValueError(
                f"OpenAI refused to generate a completion! Reason: {response_message["refusal"]}"
            )
        del response_message["refusal"]
        if prompt:
            del self._messages[-1]
        self.add_message(response_message)
        # to avoid user/assistant confusion in other conversations, we turn each assistant's response into a user-supplied message for other LLMs
        response_message["role"] = "user"
        return response_message

    def generate_embeddings(
        self, input: str | list[str | int | list[int]]
    ) -> list[dict[str, str | int | float]]:
        """
        generate an embedding for an input string, list of strings, list of tokens, or list of list of tokens.
        """
        # TODO: implement embeddings
        endpoint = self.endpoint + "embeddings"
        request = {"model": "text-embedding-ada-002", "input": input}
        response = requests.post(
            url=endpoint, json=request, headers=self.headers
        ).json()
        return response["data"]


class Ollama(LLM):
    def __init__(self, source: str, endpoint: str, headers: dict[str, str]) -> None:
        super().__init__(source, endpoint, headers)
        raise NotImplementedError


def main():
    client = OpenAI()
    _ = client.generate_completion("Let me know if this is working!")
    print(client._messages)
    _ = client.generate_completion("Awesome. Can you tell me a joke?")
    print(client._messages)


if __name__ == "__main__":
    main()
