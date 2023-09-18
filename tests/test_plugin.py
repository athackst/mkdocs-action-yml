import unittest
from unittest.mock import Mock, patch

from markdown import Markdown
from markdown.extensions.attr_list import AttrListExtension

from mkdocs_action_yml.plugin import ActionYmlExtension, ActionYmlPreprocessor


class TestActionYmlExtension(unittest.TestCase):
    def test_extend_markdown(self):
        # Create a mock Markdown instance
        md = Markdown()

        # Mock the AttrListExtension to simulate its presence
        with patch.object(AttrListExtension, "__init__", return_value=None):
            with patch.object(AttrListExtension, "extendMarkdown"):
                extension = ActionYmlExtension()
                extension.extendMarkdown(md)

                # Assert that the extension is registered and the preprocessors are added
                self.assertIn(extension, md.registeredExtensions)

                # Access the preprocessors dictionary and assert its length
                preprocessors_dict = md.preprocessors
                self.assertTrue("actionyml" in preprocessors_dict)


class TestActionYmlPreprocessor(unittest.TestCase):
    def test_run(self):
        # Create a mock Markdown instance
        md = Markdown()

        # Mock the AttrListExtension to simulate its presence
        with patch.object(AttrListExtension, "__init__", return_value=None):
            with patch.object(AttrListExtension, "extendMarkdown"):
                extension = ActionYmlExtension()
                extension.extendMarkdown(md)

                # Create a mock Preprocessor instance with a mock replace function
                mock_replace_func = Mock(return_value=[])
                preprocessor = ActionYmlPreprocessor(md, replace_func=mock_replace_func)

                # Run the preprocessor
                lines = [
                    "::: mkdocs-action-yml",
                    "    :path: example/action.yml",
                    "    :owner: athackst",
                ]
                preprocessor.run(lines)

                # Assert that the mock replace function is called
                mock_replace_func.assert_called_once()


if __name__ == "__main__":
    unittest.main()
