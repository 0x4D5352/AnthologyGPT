import unittest

from entities import Character


class CharacterTest(unittest.TestCase):
    def test_init(self):
        character = Character(
            "John",
            "20",
            "He/Him",
            "Bubbly and Outgoing",
            "man with brown hair and brown eyes",
        )
        self.assertEqual(
            character.__repr__(),
            "Character(name='John', age='20', gender='He/Him', personality='Bubbly and Outgoing', description='man with brown hair and brown eyes')",
        )

    def test_start_conversation(self):
        char1 = Character(
            "John",
            "20",
            "He/Him",
            "Bubbly and Outgoing",
            "man with brown hair and brown eyes",
        )

        char2 = Character(
            "Sarah",
            "21",
            "She/Her",
            "Logical and Calculating",
            "woman with green hair and blue eyes",
        )

        john_response = [
            {
                "role": "system",
                "content": "You are John (He/Him pronouns). You are a 20 year old man with brown hair and brown eyes. Your personality is Bubbly and Outgoing. You're having your 1st conversation with Sarah. You know this about them: nothing. Reply in character based on the conversation history and the context provided by the user. If the conversation has gone on long enough, end your message with the string </SCENE>.",
            }
        ]
        sarah_response = [
            {
                "role": "system",
                "content": "You are Sarah (She/Her pronouns). You are a 21 year old woman with green hair and blue eyes. Your personality is Logical and Calculating. You're having your 1st conversation with John. You know this about them: nothing. Reply in character based on the conversation history and the context provided by the user. If the conversation has gone on long enough, end your message with the string </SCENE>.",
            }
        ]
        convo_1 = char1.start_conversation(char2)
        self.assertEqual(char1._conversations[char2][convo_1]._messages, john_response)
        convo_2 = char2.start_conversation(char1)
        self.assertEqual(char2._conversations[char1][convo_2]._messages, sarah_response)

    def test_think(self):
        char = Character(
            "John",
            "20",
            "He/Him",
            "Bubbly and Outgoing",
            "man with brown hair and brown eyes",
        )
        conclusion = char.think(
            "You have just been invited to a birthday party with Sarah, and need to decide whether or not to go. You must include an explicit Yes or No in your answer."
        )
        self.assertIn("yes", conclusion.lower())

    def test_remember(self):
        char = Character(
            "John",
            "20",
            "He/Him",
            "Bubbly and Outgoing",
            "man with brown hair and brown eyes",
        )
        with self.assertRaises(NotImplementedError):
            char.remember("foo")

    def test_feel(self):
        char = Character(
            "John",
            "20",
            "He/Him",
            "Bubbly and Outgoing",
            "man with brown hair and brown eyes",
        )
        with self.assertRaises(NotImplementedError):
            char.feel("foo")

    def test_speak(self):
        char = Character(
            "John",
            "20",
            "He/Him",
            "Bubbly and Outgoing",
            "man with brown hair and brown eyes",
        )
        pass

    def test_listen(self):
        char = Character(
            "John",
            "20",
            "He/Him",
            "Bubbly and Outgoing",
            "man with brown hair and brown eyes",
        )
        char2 = Character(
            "Sarah",
            "21",
            "She/Her",
            "Logical and Calculating",
            "woman with green hair and blue eyes",
        )

        messages = [
            {
                "role": "system",
                "content": "Sarah said: 'oh wow that is so interesting'",
            }
        ]
        convo_index = char.start_conversation(char2)
        char.listen(char2, convo_index, messages)
        self.assertEqual(
            char._conversations[char2][convo_index]._messages[-1]["content"],
            "Sarah said: 'oh wow that is so interesting'",
        )


if __name__ == "__main__":
    unittest.main()
