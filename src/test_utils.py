import unittest
from utils import LLM, OpenAI


class LLMTest(unittest.TestCase):
    def test_repr(self):
        llm = LLM("foo", "http://www.example.com", {"header1": "foo", "header2": "bar"})
        self.assertEqual(
            llm.__repr__(),
            "LLM(source=foo, endpoint=http://www.example.com, headers={'header1': 'foo', 'header2': 'bar'}, _messages=[], _settings={'model': 'null', 'temperature': 1, 'top_p': 1, 'stream': False})",
        )

    def test_no_completion(self):
        llm = LLM("foo", "http://www.example.com", {"header1": "foo", "header2": "bar"})
        with self.assertRaises(NotImplementedError):
            llm.generate_completion("test", "test")

    def test_no_embeddings(self):
        llm = LLM("foo", "http://www.example.com", {"header1": "foo", "header2": "bar"})
        with self.assertRaises(NotImplementedError):
            llm.generate_embeddings("test")

    def test_add_message(self):
        message = {"role": "user", "message": "hi world"}
        llm = LLM("foo", "http://www.example.com", {"header1": "foo", "header2": "bar"})
        llm.add_message(message)
        self.assertEqual(llm._messages[-1], message)

    def test_change_settings(self):
        llm = LLM("foo", "http://www.example.com", {"header1": "foo", "header2": "bar"})
        llm.adjust_setting("foo", "bar")
        self.assertEqual(llm._settings["foo"], "bar")
        llm.adjust_setting("temperature", 0.5)
        self.assertNotEqual(llm._settings["temperature"], 1)
        with self.assertRaises(ValueError):
            llm.adjust_setting("top_p", 0.8)


class OpenAITest(unittest.TestCase):
    def test_init(self):
        open_ai = OpenAI()
        open_ai.headers["Authorization"] = "Bearer FOOBAR"
        self.assertEqual(
            open_ai.__repr__(),
            "LLM(source=OpenAI, endpoint=https://api.openai.com/v1/, headers={'Authorization': 'Bearer FOOBAR', 'Content-Type': 'application/json'}, _messages=[], _settings={'model': 'gpt-4o', 'temperature': 1, 'top_p': 1, 'stream': False})",
        )


if __name__ == "__main__":
    unittest.main()
