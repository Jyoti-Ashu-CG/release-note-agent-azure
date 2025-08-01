import unittest
import json
import os
from release_note_agent.github_client import load_mock_commits, format_commits

class TestGitHubClient(unittest.TestCase):
    def setUp(self):
        self.mock_path = "data/test_mock_commits.json"
        os.makedirs("data", exist_ok=True)
        with open(self.mock_path, "w") as f:
            json.dump([
                {"message": "feat: add login feature"},
                {"message": "fix: resolve crash on startup"}
            ], f)

    def tearDown(self):
        os.remove(self.mock_path)

    def test_load_mock_commits(self):
        commits = load_mock_commits(self.mock_path)
        self.assertIsInstance(commits, list)
        self.assertTrue(all(isinstance(msg, str) for msg in commits))
        self.assertGreater(len(commits), 0)

    def test_format_commits(self):
        raw_commits = [
            "feat: add login feature",
            "fix: resolve crash on startup",
            "docs: update README",
            "refactor: cleanup auth logic"
        ]
        formatted = format_commits(raw_commits)
        self.assertIn("### Features", formatted)
        self.assertIn("### Bug Fixes", formatted)
        self.assertIn("- feat: add login feature", formatted)

if __name__ == "__main__":
    unittest.main()