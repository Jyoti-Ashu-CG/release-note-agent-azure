import unittest
from release_note_agent.generator import ReleaseNoteGenerator

class MockChain:
    def invoke(self, inputs):
        return f"# Release Notes\n\n{inputs['commits']}"

class TestReleaseNoteGenerator(unittest.TestCase):
    def test_generate(self):
        generator = ReleaseNoteGenerator(openai_api_key="fake-key")
        generator.chain = MockChain()  # Mocking the chain
        result = generator.generate("### Features\n- feat: add search")
        self.assertIn("### Features", result)
        self.assertIn("feat: add search", result)

if __name__ == "__main__":
    unittest.main()