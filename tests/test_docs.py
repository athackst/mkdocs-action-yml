import os
import unittest

from mkdocs_action_yml._docs import (
    _format_table_inputs_row,
    _format_table_outputs_row,
    _format_usage_row,
    _make_description,
    _make_runs,
    _make_table_inputs,
    _make_table_outputs,
    _make_title,
    _make_usage,
    make_action_docs,
)


class TestDocsUtils(unittest.TestCase):
    def test_make_title(self):
        title = _make_title("My Action")
        self.assertEqual(list(title), ["# My Action", ""])

    def test_make_description(self):
        description = _make_description("This is a test action.")
        self.assertEqual(list(description), ["This is a test action.", ""])

    def test_make_runs(self):
        description = _make_runs({"using": "composite"})
        self.assertEqual(list(description), ["This action is a composite action.", ""])

    def test_format_usage_row_required(self):
        input_data = {"required": True, "default": "default_value"}
        usage_row = _format_usage_row("input_name", input_data)
        self.assertEqual(usage_row, "           input_name: default_value")

    def test_format_usage_row_optional(self):
        input_data = {"required": False, "default": "default_value"}
        usage_row = _format_usage_row("input_name", input_data)
        self.assertEqual(usage_row, "           input_name: default_value # optional")

    def test_make_table_inputs(self):
        inputs = {"input1": {"required": True, "default": "value1", "description": "Description1"}}
        table = _make_table_inputs(inputs)
        expected_table = [
            "## Inputs",
            "",
            "| Input | Description | Default |",
            "| ----- | ----------- | ------- |",
            "| input1 | [required] Description1 | `value1` |",
            "",
        ]
        self.assertEqual(list(table), expected_table)

    def test_format_table_inputs_row(self):
        input_data = {"required": True, "default": "value1", "description": "Description1"}
        row = _format_table_inputs_row("input1", input_data)
        self.assertEqual(row, "| input1 | [required] Description1 | `value1` |")

    def test_make_table_outputs(self):
        outputs = {"output1": {"description": "Output Description", "value": "output_value"}}
        table = _make_table_outputs(outputs)
        expected_table = [
            "## Outputs",
            "",
            "| Output | Description |",
            "| ------ | ----------- |",
            "| output1 | Output Description |",
            "",
        ]
        self.assertEqual(list(table), expected_table)

    def test_format_table_outputs_row(self):
        output_data = {"description": "Output Description", "value": "output_value"}
        row = _format_table_outputs_row("output1", output_data)
        self.assertEqual(row, "| output1 | Output Description |")

    def test_make_usage(self):
        action_file = "test_action.yml"
        owner = "test_owner"
        version = "v1"
        inputs = {"input1": {"required": True, "default": "value1"}}
        usage = _make_usage(owner, action_file, version, inputs)
        expected_usage = [
            "## Usage",
            "",
            "```yaml",
            "name: Example usage",
            "on: push",
            "jobs:",
            "  example_job:",
            "    runs-on: ubuntu-latest",
            "    steps:",
            f"      - uses: {owner}/{os.path.splitext(os.path.basename(action_file))[0]}@{version}",
            "         with:",
            "           input1: value1",
            "```",
            "",
        ]
        self.assertEqual(list(usage), expected_usage)


class TestActionDocs(unittest.TestCase):
    def test_make_action_docs(self):
        action_file = "tests/test_action.yml"
        owner = "test_owner"
        version = "v1"

        # Create a temporary action.yml file for testing
        with open(action_file, "w") as f:
            f.write(
                "name: Test Action\n"
                "description: This is a test action\n"
                "inputs:\n"
                "  input1:\n"
                "    required: true\n"
                "    default: 'default_value'\n"
                "    description: Input description\n"
                "outputs:\n"
                "  output1:\n"
                "    description: Output description\n"
                "    value: 'output_value'\n"
                "runs:\n"
                "  using: composite\n"
            )

        result = list(make_action_docs(action_file, owner, version))

        expected_result = [
            "# Test Action",
            "",
            "This is a test action",
            "",
            "This action is a composite action.",
            "",
            "## Inputs",
            "",
            "| Input | Description | Default |",
            "| ----- | ----------- | ------- |",
            "| input1 | [required] Input description | `default_value` |",
            "",
            "## Outputs",
            "",
            "| Output | Description |",
            "| ------ | ----------- |",
            "| output1 | Output description |",
            "",
            "## Usage",
            "",
            "```yaml",
            "name: Example usage",
            "on: push",
            "jobs:",
            "  example_job:",
            "    runs-on: ubuntu-latest",
            "    steps:",
            f"      - uses: {owner}/{os.path.splitext(os.path.basename(action_file))[0]}@{version}",
            "         with:",
            "           input1: default_value",
            "```",
            "",
        ]

        self.assertEqual(result, expected_result)

        # Clean up temporary action.yml file
        os.remove(action_file)

    def test_make_action_docs_no_inputs_no_outputs(self):
        action_file = "test_action.yml"
        owner = "test_owner"
        version = "v1"

        # Create a temporary action.yml file for testing
        with open(action_file, "w") as f:
            f.write(
                "name: Test Action\n"
                "description: This is a test action\n"
                "runs:\n"
                "  using: composite\n"
            )

        result = list(make_action_docs(action_file, owner, version))

        expected_result = [
            "# Test Action",
            "",
            "This is a test action",
            "",
            "This action is a composite action.",
            "",
            "## Usage",
            "",
            "```yaml",
            "name: Example usage",
            "on: push",
            "jobs:",
            "  example_job:",
            "    runs-on: ubuntu-latest",
            "    steps:",
            f"      - uses: {owner}/{os.path.splitext(os.path.basename(action_file))[0]}@{version}",
            "```",
            "",
        ]

        self.assertEqual(result, expected_result)

        # Clean up temporary action.yml file
        os.remove(action_file)

    def test_make_action_docs_with_inputs_no_outputs(self):
        action_file = "test_action.yml"
        owner = "test_owner"
        version = "v1"

        # Create a temporary action.yml file for testing
        with open(action_file, "w") as f:
            f.write(
                "name: Test Action\n"
                "description: This is a test action\n"
                "inputs:\n"
                "  input1:\n"
                "    required: true\n"
                "    default: 'default_value'\n"
                "    description: Input description\n"
                "runs:\n"
                "  using: composite\n"
            )

        result = list(make_action_docs(action_file, owner, version))

        expected_result = [
            "# Test Action",
            "",
            "This is a test action",
            "",
            "This action is a composite action.",
            "",
            "## Inputs",
            "",
            "| Input | Description | Default |",
            "| ----- | ----------- | ------- |",
            "| input1 | [required] Input description | `default_value` |",
            "",
            "## Usage",
            "",
            "```yaml",
            "name: Example usage",
            "on: push",
            "jobs:",
            "  example_job:",
            "    runs-on: ubuntu-latest",
            "    steps:",
            f"      - uses: {owner}/{os.path.splitext(os.path.basename(action_file))[0]}@{version}",
            "         with:",
            "           input1: default_value",
            "```",
            "",
        ]

        self.assertEqual(result, expected_result)

        # Clean up temporary action.yml file
        os.remove(action_file)

    def test_make_action_docs_no_inputs_with_outputs(self):
        action_file = "test_action.yml"
        owner = "test_owner"
        version = "v1"

        # Create a temporary action.yml file for testing
        with open(action_file, "w") as f:
            f.write(
                "name: Test Action\n"
                "description: This is a test action\n"
                "outputs:\n"
                "  output1:\n"
                "    description: Output description\n"
                "    value: 'output_value'\n"
                "runs:\n"
                "  using: composite\n"
            )

        result = list(make_action_docs(action_file, owner, version))

        expected_result = [
            "# Test Action",
            "",
            "This is a test action",
            "",
            "This action is a composite action.",
            "",
            "## Outputs",
            "",
            "| Output | Description |",
            "| ------ | ----------- |",
            "| output1 | Output description |",
            "",
            "## Usage",
            "",
            "```yaml",
            "name: Example usage",
            "on: push",
            "jobs:",
            "  example_job:",
            "    runs-on: ubuntu-latest",
            "    steps:",
            f"      - uses: {owner}/{os.path.splitext(os.path.basename(action_file))[0]}@{version}",
            "```",
            "",
        ]

        self.assertEqual(result, expected_result)

        # Clean up temporary action.yml file
        os.remove(action_file)

    def test_make_action_docs_missing_required(self):
        action_file = "test_action.yml"
        owner = "test_owner"
        version = "v1"

        # Create a temporary action.yml file for testing with missing 'required'
        with open(action_file, "w") as f:
            f.write(
                "name: Test Action\n"
                "description: This is a test action\n"
                "inputs:\n"
                "  input1:\n"
                "    default: 'default_value'\n"
                "    description: Input description\n"
                "runs:\n"
                "  using: composite\n"
            )
        result = list(make_action_docs(action_file, owner, version))

        expected_result = [
            "# Test Action",
            "",
            "This is a test action",
            "",
            "This action is a composite action.",
            "",
            "## Inputs",
            "",
            "| Input | Description | Default |",
            "| ----- | ----------- | ------- |",
            "| input1 | [optional] Input description | `default_value` |",
            "",
            "## Usage",
            "",
            "```yaml",
            "name: Example usage",
            "on: push",
            "jobs:",
            "  example_job:",
            "    runs-on: ubuntu-latest",
            "    steps:",
            f"      - uses: {owner}/{os.path.splitext(os.path.basename(action_file))[0]}@{version}",
            "         with:",
            "           input1: default_value # optional",
            "```",
            "",
        ]

        self.assertEqual(result, expected_result)

        # Clean up temporary action.yml file
        os.remove(action_file)

    def test_make_action_docs_missing_default(self):
        action_file = "test_action.yml"
        owner = "test_owner"
        version = "v1"

        # Create a temporary action.yml file for testing with missing 'default'
        with open(action_file, "w") as f:
            f.write(
                "name: Test Action\n"
                "description: This is a test action\n"
                "inputs:\n"
                "  input1:\n"
                "    required: true\n"
                "    description: Input description\n"
                "runs:\n"
                "  using: composite\n"
            )
        result = list(make_action_docs(action_file, owner, version))

        expected_result = [
            "# Test Action",
            "",
            "This is a test action",
            "",
            "This action is a composite action.",
            "",
            "## Inputs",
            "",
            "| Input | Description | Default |",
            "| ----- | ----------- | ------- |",
            "| input1 | [required] Input description | `` |",
            "",
            "## Usage",
            "",
            "```yaml",
            "name: Example usage",
            "on: push",
            "jobs:",
            "  example_job:",
            "    runs-on: ubuntu-latest",
            "    steps:",
            f"      - uses: {owner}/{os.path.splitext(os.path.basename(action_file))[0]}@{version}",
            "         with:",
            "           input1: ",
            "```",
            "",
        ]

        self.assertEqual(result, expected_result)

        # Clean up temporary action.yml file
        os.remove(action_file)


if __name__ == "__main__":
    unittest.main()
