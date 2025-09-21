"""unittest file."""
import os
import json
import unittest
from click.testing import CliRunner
from ink import commands


class TestInkCLI(unittest.TestCase):
    """The Ink CLI commands test class."""
    def setUp(self):
        """Setup a temporary test environment"""
        self.runner = CliRunner()

        self.test_file = ".test_notes.json"
        commands.NOTE_FILE = self.test_file
        if os.path.exists(self.test_file):
            os.remove(self.test_file)

    def tearDown(self):
        """Clean up the test file."""
        if os.path.exists(self.test_file):
            os.remove(self.test_file)

    def _add_note(self, title="TestNote", content="Sample Content", tags="cli,test"):
        """Helper method to add a note"""
        return self.runner.invoke(
            commands.add,
            [title, "--content", content, "--tags", tags]
        )

    def test_add_note(self):
        """Test method for adding a note."""
        result = self._add_note()
        self.assertEqual(result.exit_code, 0)
        self.assertIn("Note 'TestNote' added!", result.output)

        with open(self.test_file, "r", encoding="utf-8") as file:
            notes = json.load(file)
        self.assertEqual(len(notes), 1)
        self.assertEqual(notes[0]["content"], "Sample Content")

    def test_list_empty_notes(self):
        """Test method for listing notes when none exist."""
        result = self.runner.invoke(commands.lst)
        self.assertIn("No notes found.", result.output)

    def test_list_notes(self):
        """Test method for listing notes when some exist."""
        self._add_note("Meeting", "Discuss roadmap", "work")
        result = self.runner.invoke(commands.lst)
        self.assertIn("Meeting.txt", result.output)

    def test_view_note(self):
        """Test method for viewing a note."""
        self._add_note("ViewTest", "This is viewable content")
        with open(self.test_file, "r", encoding="utf-8") as file:
            note_id = json.load(file)[0]["id"]

        result = self.runner.invoke(commands.view, [str(note_id)])
        self.assertIn("This is viewable content", result.output)

    def test_view_note_not_found(self):
        """Test method for viewing a non-existent note."""
        result = self.runner.invoke(commands.view, ["12345"])
        self.assertIn("Note not found.", result.output)

    def test_delete_note(self):
        """Test method for deleting a note."""
        self._add_note("DeleteTest", "Remove")
        with open(self.test_file, "r", encoding="utf-8") as file:
            note_id = json.load(file)[0]["id"]

        result = self.runner.invoke(commands.delete, [str(note_id)])
        self.assertIn("Note deleted", result.output)

        with open(self.test_file, "r", encoding="utf-8") as file:
            notes = json.load(file)
        self.assertEqual(len(notes), 0)

    def test_delete_note_not_found(self):
        """Test method for deleting a non-existent note."""
        result = self.runner.invoke(commands.delete, ["12345"])
        self.assertIn("Note not found.", result.output)

    def test_search_notes(self):
        """Test method for searching notes."""
        self._add_note("SearchTest", "This content is searchable")
        result = self.runner.invoke(commands.search, ["searchable"])
        self.assertIn("SearchTest.txt", result.output)

    def test_search_no_results(self):
        """Test method for searching notes with no results."""
        self._add_note("OtherNote", "Completely unrelated")
        result = self.runner.invoke(commands.search, ["missing"])
        self.assertIn("No matching notes found.", result.output)


if __name__ == "__main__":
    unittest.main()
