import unittest
from textwrap import dedent

from mkdocs_action_yml._processing import replace_blocks


class TestReplaceOptions(unittest.TestCase):
    def test_replace_options(self):
        source = dedent(
            """
            # Some content
            foo
            ::: target
                :option1: value1
                :optiøn2: value2
            \t:option3:
                :option4:\x20
            bar
            """
        ).strip()

        expected = dedent(
            """
            # Some content
            foo
            {'option1': 'value1', 'optiøn2': 'value2', 'option3': '', 'option4': ''}
            bar
            """
        ).strip()

        output = list(
            replace_blocks(
                source.splitlines(), title="target", replace=lambda **options: [str(options)]
            )
        )
        self.assertEqual(output, expected.splitlines())

    def test_replace_no_options(self):
        source = dedent(
            """
            # Some content
            foo
            ::: target
            bar
            """
        ).strip()

        expected = dedent(
            """
            # Some content
            foo
            > mock
            bar
            """
        ).strip()

        output = list(
            replace_blocks(
                source.splitlines(), title="target", replace=lambda **options: ["> mock"]
            )
        )
        self.assertEqual(output, expected.splitlines())

    def test_other_blocks_unchanged(self):
        source = dedent(
            """
            # Some content
            ::: target
            ::: plugin1
                :option1: value1
            ::: target
                :option: value
            ::: plugin2
                :option2: value2
            bar
            """
        ).strip()

        expected = dedent(
            """
            # Some content
            ::: plugin1
                :option1: value1
            ::: plugin2
                :option2: value2
            bar
            """
        ).strip()

        output = list(
            replace_blocks(source.splitlines(), title="target", replace=lambda **kwargs: [])
        )
        self.assertEqual(output, expected.splitlines())


if __name__ == "__main__":
    unittest.main()
