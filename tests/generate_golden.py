import os
from pathlib import Path

from markdown import Markdown

import mkdocs_action_yml

FIXTURES_DIR = os.path.join("tests", "fixtures")
EXAMPLE_DIR = os.path.join("docs")
GOLDEN_DIR = os.path.join("golden")


def _get_test_files() -> str:
    # Get all .md files in the app directory
    for root, _, files in os.walk(EXAMPLE_DIR):
        for file in files:
            if file.endswith(".md"):
                yield os.path.join(root, file)


def _generate_golden_file(input_file: str) -> None:
    # Create the golden file from the test file.
    input_basename = os.path.basename(input_file)
    golden_filename = f"{input_basename}.golden"
    golden_file_path = os.path.join(GOLDEN_DIR, golden_filename)

    md = Markdown(extensions=[mkdocs_action_yml.makeExtension()])

    source = Path(input_file).read_text()

    with open(golden_file_path, "w") as golden_file:
        golden_file.write(md.convert(source))


def generate_golden() -> None:
    # Change the current working directory to FIXTURES_DIR
    os.chdir(FIXTURES_DIR)
    for test_file in _get_test_files():
        _generate_golden_file(test_file)


if __name__ == "__main__":
    generate_golden()
