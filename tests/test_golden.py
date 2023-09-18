import os
import unittest
from pathlib import Path

from markdown import Markdown

import mkdocs_action_yml

# Get the absolute path of the directory containing the test script
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
FIXTURES_DIR = os.path.join(SCRIPT_DIR, "fixtures")
EXAMPLE_DIR = os.path.join(FIXTURES_DIR, "docs")
GOLDEN_DIR = os.path.join(FIXTURES_DIR, "golden")


def create_test_method(fixtures_dir, input_filename, expected_filename):
    def test_method(self):
        md = Markdown(extensions=[mkdocs_action_yml.makeExtension()])

        # Change the current working directory to FIXTURES_DIR
        os.chdir(fixtures_dir)

        input_path = Path(input_filename)
        expected_path = Path(expected_filename)

        with input_path.open("r") as input_file, expected_path.open("r") as expected_file:
            source = input_file.read()
            expected = expected_file.read()

        self.assertEqual(md.convert(source), expected)

    return test_method


class TestExtension(unittest.TestCase):
    pass


for golden_file in Path(GOLDEN_DIR).glob("*.golden"):
    input_filename = Path(os.path.join(EXAMPLE_DIR, golden_file.stem)).relative_to(FIXTURES_DIR)
    expected_filename = Path(os.path.join(GOLDEN_DIR, golden_file.name)).relative_to(FIXTURES_DIR)

    test_method = create_test_method(FIXTURES_DIR, input_filename, expected_filename)
    test_name = f"test_golden_{input_filename}"
    setattr(TestExtension, test_name, test_method)

if __name__ == "__main__":
    unittest.main()
